
import { NextResponse } from "next/server";

type GitTreeItem = {
  path: string;
  type: "tree" | "blob" | "commit";
};

type TreeNode = {
  name: string;
  path: string;
  type: "folder" | "file";
  url: string;
  children: TreeNode[];
};

const owner = process.env.GITHUB_OWNER!;
const repo = process.env.GITHUB_REPO!;
const token = process.env.GITHUB_TOKEN;

async function githubFetch(path: string) {
  const response = await fetch(
    `https://api.github.com${path}`,
    {
      headers: {
        Accept: "application/vnd.github+json",
        ...(token
          ? { Authorization: `Bearer ${token}` }
          : {}),
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error(`GitHub API: ${response.status}`);
  }

  return response.json();
}

export async function GET() {
  try {
    const repoInfo = await githubFetch(
      `/repos/${owner}/${repo}`
    );

    const branch =
      process.env.GITHUB_BRANCH ||
      repoInfo.default_branch;

    const encodedBranch = encodeURIComponent(branch);

    const result = await githubFetch(
      `/repos/${owner}/${repo}/git/trees/${encodedBranch}?recursive=1`
    );

    if (result.truncated) {
      throw new Error("GitHub tree result truncated");
    }

    const roots: TreeNode[] = [];
    const folders = new Map<string, TreeNode>();

    const items = (result.tree as GitTreeItem[])
      .filter(
        (item) =>
          item.type === "tree" ||
          item.type === "blob"
      )
      .sort(
        (a, b) =>
          a.path.split("/").length -
          b.path.split("/").length
      );

    for (const item of items) {
      const parts = item.path.split("/");
      const name = parts.at(-1)!;
      const isFolder = item.type === "tree";

      const node: TreeNode = {
        name,
        path: item.path,
        type: isFolder ? "folder" : "file",
        url: `https://github.com/${owner}/${repo}/${isFolder ? "tree" : "blob"}/${encodedBranch}/${parts.map(encodeURIComponent).join("/")}`,
        children: [],
      };

      if (isFolder) {
        folders.set(item.path, node);
      }

      const parentPath = parts.slice(0, -1).join("/");
      const parent = folders.get(parentPath);

      if (parent) {
        parent.children.push(node);
      } else {
        roots.push(node);
      }
    }

    const sortTree = (nodes: TreeNode[]) => {
      nodes.sort(
        (a, b) =>
          (a.type === "folder" ? 0 : 1) -
            (b.type === "folder" ? 0 : 1) ||
          a.name.localeCompare(b.name)
      );
      nodes.forEach((node) => sortTree(node.children));
    };

    sortTree(roots);

    return NextResponse.json({
      name: repo,
      branch,
      tree: roots,
    });
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { error: "Failed to load GitHub repository" },
      { status: 500 }
    );
  }
}
