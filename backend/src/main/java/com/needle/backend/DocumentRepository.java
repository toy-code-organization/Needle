package com.needle.backend;

import org.springframework.data.jpa.repository.JpaRepository;

// 문서를 DB에 저장하고 조회
public interface DocumentRepository extends JpaRepository<Document, Integer> {
}
