
"use client";

import { useEffect, useState } from "react";

type TreeNode = {
  name: string;
  path: string;
  type: "folder" | "file";
  url: string;
  children: TreeNode[];
};

type TreeResponse = {
  name: string;
  branch: string;
  tree: TreeNode[];
};

function TreeItem({
  node,
  level = 0,
}: {
  node: TreeNode;
  level?: number;
}) {
  const [open, setOpen] = useState(level < 1);
  const folder = node.type === "folder";

  return (
    <div>
      <div
        style={{
          paddingLeft: level * 18 + 8,
          display: "flex",
          alignItems: "center",
          gap: 8,
          minHeight: 32,
          fontSize: 14,
        }}
      >
        <button
          onClick={() => setOpen(!open)}
          disabled={!folder}
          style={{
            border: "none",
            background: "none",
            cursor: folder ? "pointer" : "default",
            width: 18,
          }}
        >
          {folder ? (open ? "⌄" : "›") : ""}
        </button>

        <span>{folder ? (open ? "📂" : "📁") : "📄"}</span>

        <a
          href={node.url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: "inherit",
            textDecoration: "none",
          }}
        >
          {node.name}
        </a>
      </div>

      {folder && open &&
        node.children.map((child) => (
          <TreeItem
            key={child.path}
            node={child}
            level={level + 1}
          />
        ))}
    </div>
  );
}

export default function Home() {
  const [data, setData] = useState<TreeResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  async function refresh() {
    try {
      const response = await fetch("/api/tree", {
        cache: "no-store",
      });

      if (!response.ok) throw new Error();

      const result = await response.json();
      setData(result);
      setError("");
    } catch {
      setError("GitHub 레포지토리를 불러오지 못했습니다.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();

    const interval = setInterval(refresh, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main
      style={{
        padding: 20,
        fontFamily: "Arial, sans-serif",
        color: "#333",
      }}
    >
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <div>
          <h2 style={{ margin: 0, fontSize: 18 }}>
            📦 {data?.name ?? "GitHub Repository"}
          </h2>
          {data && (
            <small>Branch: {data.branch}</small>
          )}
        </div>

        <button onClick={refresh}>↻ 새로고침</button>
      </header>

      {loading && <p>불러오는 중...</p>}
      {error && <p>{error}</p>}

      {data?.tree.map((node) => (
        <TreeItem key={node.path} node={node} />
      ))}
    </main>
  );
}
