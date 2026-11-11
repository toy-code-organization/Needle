package com.needle.backend;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

// DB의 문서 한 건을 표현
@Entity
@Table(name = "documents", schema = "backend")
public class Document {
    // 문서 번호는 DB에서 자동으로 생성
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, columnDefinition = "text")
    private String filename;

    @Column(nullable = false, columnDefinition = "text")
    private String content;

    // JPA가 객체를 생성할 때 사용하는 기본 생성자
    protected Document() {
    }

    // 업로드한 파일명과 내용을 문서에 포함
    public Document(String filename, String content) {
        this.filename = filename;
        this.content = content;
    }

    // 저장된 문서의 값을 조회
    public Integer getId() { return id; }
    public String getFilename() { return filename; }
    public String getContent() { return content; }
}
