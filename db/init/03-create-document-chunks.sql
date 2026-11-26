CREATE TABLE ai.document_chunks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- backend.documents.id 참조 예정. 외래키는 팀 합의 후 추가
    document_id INTEGER NOT NULL,
    document_version INTEGER NOT NULL,
    chunk_order INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(1024) NOT NULL,
    source_location TEXT NOT NULL,
    model_name TEXT NOT NULL,

    CONSTRAINT document_chunks_document_version_check
        CHECK (document_version >= 1),
    CONSTRAINT document_chunks_chunk_order_check
        CHECK (chunk_order >= 0),
    CONSTRAINT document_chunks_chunk_text_not_blank_check
        CHECK (chunk_text ~ '[^[:space:]]'),
    CONSTRAINT document_chunks_document_version_chunk_order_key
        UNIQUE (document_id, document_version, chunk_order)
);
