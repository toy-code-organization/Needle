package com.needle.backend;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Locale;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

// 업로드 파일을 검사하고 문서 저장과 조회를 처리
@Service
public class DocumentService {
    private final DocumentRepository repository;

    public DocumentService(DocumentRepository repository) {
        this.repository = repository;
    }

    // 파일이 유효하면 이름과 내용을 DB에 저장
    @Transactional
    public Document upload(MultipartFile file) {
        String original = file.getOriginalFilename();
        if (original == null || original.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "파일 이름이 필요합니다.");
        }
        // 파일명에 경로가 포함되어 있으면 마지막 이름만 사용
        String filename = original.replace('\\', '/');
        filename = filename.substring(filename.lastIndexOf('/') + 1);
        // TXT 파일만 받고, 빈 파일과 1MB 초과 파일은 거절
        if (!filename.toLowerCase(Locale.ROOT).endsWith(".txt") || filename.length() <= 4) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "TXT 파일만 업로드할 수 있습니다.");
        }
        if (file.isEmpty() || file.getSize() > 1024 * 1024) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "파일은 비어 있지 않아야 하며 1MB 이하여야 합니다.");
        }
        try {
            // 파일을 UTF-8 텍스트로 읽고 잘못된 문자는 거절
            String content = StandardCharsets.UTF_8.newDecoder()
                    .onMalformedInput(CodingErrorAction.REPORT)
                    .onUnmappableCharacter(CodingErrorAction.REPORT)
                    .decode(ByteBuffer.wrap(file.getBytes())).toString();
            // PostgreSQL 텍스트에 저장할 수 없는 NUL 문자를 검사
            if (content.indexOf('\0') >= 0) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "올바른 텍스트 파일이 아닙니다.");
            }
            return repository.save(new Document(filename, content));
        } catch (CharacterCodingException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "UTF-8로 저장된 TXT 파일이 필요합니다.", e);
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "파일을 읽지 못했습니다.", e);
        }
    }

    // 저장된 전체 문서를 조회합니다.
    @Transactional(readOnly = true)
    public List<Document> findAll() {
        return repository.findAll();
    }
}
