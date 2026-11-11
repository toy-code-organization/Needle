package com.needle.backend;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

// 문서 관련 HTTP 요청을 처리합니다.
@RestController
@RequestMapping("/api/documents")
public class DocumentController {
    private final DocumentService service;

    public DocumentController(DocumentService service) {
        this.service = service;
    }

    // multipart 요청의 file 항목을 받아 문서를 저장합니다.
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @ResponseStatus(HttpStatus.CREATED)
    public Document upload(@RequestPart("file") MultipartFile file) {
        return service.upload(file);
    }

    // 저장된 문서 목록을 반환합니다.
    @GetMapping
    public List<Document> list() {
        return service.findAll();
    }
}
