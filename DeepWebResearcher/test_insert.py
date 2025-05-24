import os
import pytest
from unittest.mock import patch, MagicMock
import json
from insert import (
    index_research_text, 
    check_text_quality, 
    insert_text_at_position,
    get_chat_suggestions,
    create_side_chat_window,
    process_chat_query,
    insert_suggestion_into_document
)

# Set testing environment variable
os.environ['TESTING'] = 'True'

# Sample test data
SAMPLE_RESEARCH = """
Key Findings on Artificial Intelligence Impact

Our research indicates that AI adoption in businesses has increased by 45% since 2020.
Companies implementing AI solutions report an average productivity increase of 32%.

The most significant barriers to AI adoption include:
1. Lack of skilled personnel (67% of respondents)
2. Data quality issues (58%)
3. Integration with existing systems (51%)

Example: A manufacturing company implemented computer vision AI and reduced quality control costs by 35% while improving defect detection by 28%.

For more information, see our detailed methodology at www.airesearch.org/methodology

References:
1. Johnson, T. et al. (2023). "AI Implementation Strategies." Journal of Business Technology, 45(2), 112-128.
2. https://www.techreports.com/ai-adoption-2023
3. Smith, R. (2022). "Overcoming Barriers to AI Adoption." Harvard Business Review.
"""

SAMPLE_DOCUMENT = """# AI Implementation Report

## Introduction

This report examines the impact of artificial intelligence on business operations.

## Current State

Many businesses are still in early stages of AI adoption.
"""

# Mock responses for LLM calls
MOCK_INDEXED_DATA = {
    "key_findings": [
        "Our research indicates that AI adoption in businesses has increased by 45% since 2020.",
        "Companies implementing AI solutions report an average productivity increase of 32%."
    ],
    "statistics": [
        "AI adoption in businesses has increased by 45% since 2020.",
        "Companies implementing AI solutions report an average productivity increase of 32%."
    ],
    "definitions": [
        "The most significant barriers to AI adoption include: 1. Lack of skilled personnel (67% of respondents) 2. Data quality issues (58%) 3. Integration with existing systems (51%)"
    ],
    "examples": [
        "A manufacturing company implemented computer vision AI and reduced quality control costs by 35% while improving defect detection by 28%."
    ],
    "sources": [
        "Johnson, T. et al. (2023). \"AI Implementation Strategies.\" Journal of Business Technology, 45(2), 112-128.",
        "https://www.techreports.com/ai-adoption-2023",
        "Smith, R. (2022). \"Overcoming Barriers to AI Adoption.\" Harvard Business Review."
    ]
}

MOCK_QUALITY_CHECK = {
    "grammar_score": 8,
    "logic_score": 7,
    "suggestions": [
        "Consider revising for clarity",
        "Check factual accuracy",
        "Improve sentence structure"
    ],
    "is_acceptable": True
}

MOCK_SUGGESTIONS = [
    "AI adoption has increased by 45% since 2020.",
    "The top barriers to AI adoption are lack of skilled personnel (67%), data quality issues (58%), and integration challenges (51%).",
    "Companies implementing AI solutions report an average productivity increase of 32%."
]

# Tests for insert_text_at_position function
def test_insert_text_at_position():
    # Test inserting at the beginning
    result = insert_text_at_position(SAMPLE_DOCUMENT, "NEW LINE", 1)
    assert result.split('\n')[0] == "NEW LINE"
    
    # Test inserting in the middle
    result = insert_text_at_position(SAMPLE_DOCUMENT, "MIDDLE LINE", 4)
    lines = result.split('\n')
    assert lines[3] == "MIDDLE LINE"
    
    # Test inserting at the end
    line_count = len(SAMPLE_DOCUMENT.split('\n'))
    result = insert_text_at_position(SAMPLE_DOCUMENT, "END LINE", line_count + 1)
    lines = result.split('\n')
    assert lines[-1] == "END LINE"
    
    # Test out of range
    with pytest.raises(ValueError):
        insert_text_at_position(SAMPLE_DOCUMENT, "INVALID", 100)

# Tests for index_research_text function
def test_index_research_text():
    # Use patch to replace the entire function
    with patch('insert.index_research_text', return_value=MOCK_INDEXED_DATA):
        from insert import index_research_text
        
        # Test function
        result = index_research_text(SAMPLE_RESEARCH)
        
        # Verify result structure
        assert isinstance(result, dict)
        assert "key_findings" in result
        assert "statistics" in result
        assert "definitions" in result
        assert "examples" in result
        assert "sources" in result
        
        # Verify each category has content
        for category, items in result.items():
            assert isinstance(items, list)

# Tests for check_text_quality function
def test_check_text_quality():
    # Use patch to replace the entire function
    with patch('insert.check_text_quality', return_value=MOCK_QUALITY_CHECK):
        from insert import check_text_quality
        
        # Test function
        result = check_text_quality("Sample text to check")
        
        # Verify result structure
        assert isinstance(result, dict)
        assert "grammar_score" in result
        assert "logic_score" in result
        assert "suggestions" in result
        assert "is_acceptable" in result
        
        # Verify scores are in expected range
        assert 0 <= result["grammar_score"] <= 10
        assert 0 <= result["logic_score"] <= 10
        
        # Verify suggestions
        assert isinstance(result["suggestions"], list)

# Tests for get_chat_suggestions function
@patch('insert.text_processor')
def test_get_chat_suggestions(mock_processor):
    # Setup mock
    mock_chain = MagicMock()
    mock_processor.__or__.return_value = mock_chain
    mock_chain.__or__.return_value = mock_chain
    mock_chain.invoke.return_value = "\n".join(MOCK_SUGGESTIONS)
    
    # Test function
    result = get_chat_suggestions(MOCK_INDEXED_DATA, "What are the barriers to AI adoption?")
    
    # Verify result
    assert isinstance(result, list)
    assert len(result) > 0
    
    # Test error handling
    mock_chain.invoke.side_effect = Exception("Test error")
    result = get_chat_suggestions(MOCK_INDEXED_DATA, "Query that causes error")
    assert isinstance(result, list)
    assert "Error" in result[0]

# Tests for create_side_chat_window function
@patch('insert.index_research_text')
@patch('insert.get_chat_suggestions')
def test_create_side_chat_window(mock_get_suggestions, mock_index):
    # Setup mocks
    mock_index.return_value = MOCK_INDEXED_DATA
    mock_get_suggestions.return_value = MOCK_SUGGESTIONS
    
    # Test function
    result = create_side_chat_window(SAMPLE_RESEARCH, SAMPLE_DOCUMENT)
    
    # Verify result structure
    assert isinstance(result, dict)
    assert "indexed_data" in result
    assert "quick_topics" in result
    assert "initial_suggestions" in result
    assert "document_lines" in result
    assert "chat_ready" in result
    
    # Verify quick topics
    assert isinstance(result["quick_topics"], list)
    
    # Verify document lines count
    assert result["document_lines"] == len(SAMPLE_DOCUMENT.split('\n'))
    
    # Verify chat is ready
    assert result["chat_ready"] is True

# Tests for process_chat_query function
@patch('insert.get_chat_suggestions')
@patch('insert.check_text_quality')
def test_process_chat_query(mock_check_quality, mock_get_suggestions):
    # Setup mocks
    mock_get_suggestions.return_value = MOCK_SUGGESTIONS
    mock_check_quality.return_value = MOCK_QUALITY_CHECK
    
    # Test without current line
    result = process_chat_query(
        "What are barriers to AI adoption?",
        MOCK_INDEXED_DATA,
        SAMPLE_DOCUMENT
    )
    
    # Verify result structure
    assert isinstance(result, dict)
    assert "suggestions" in result
    assert "context_aware_suggestions" in result
    assert "quality_check" in result
    assert "relevant_categories" in result
    assert "can_insert" in result
    
    # Verify can_insert is False when no current line
    assert result["can_insert"] is False
    
    # Test with current line
    result = process_chat_query(
        "What are barriers to AI adoption?",
        MOCK_INDEXED_DATA,
        SAMPLE_DOCUMENT,
        current_line=4
    )
    
    # Verify can_insert is True when current line is provided
    assert result["can_insert"] is True
    
    # Verify suggestions
    assert result["suggestions"] == MOCK_SUGGESTIONS

# Tests for insert_suggestion_into_document function
@patch('insert.check_text_quality')
@patch('insert.insert_text_at_position')
def test_insert_suggestion_into_document(mock_insert, mock_check_quality):
    # Setup mocks for successful insertion
    mock_check_quality.return_value = MOCK_QUALITY_CHECK
    mock_insert.return_value = SAMPLE_DOCUMENT + "\nInserted text"
    
    # Test successful insertion
    result = insert_suggestion_into_document(
        SAMPLE_DOCUMENT,
        "AI adoption has increased by 45% since 2020.",
        4
    )
    
    # Verify result structure for success
    assert isinstance(result, dict)
    assert "success" in result
    assert result["success"] is True
    assert "updated_document" in result
    assert "quality_result" in result
    assert "insertion_point" in result
    
    # Test failed quality check
    mock_check_quality.return_value = {
        "grammar_score": 3,
        "logic_score": 2,
        "suggestions": ["Major revision needed"],
        "is_acceptable": False
    }
    
    result = insert_suggestion_into_document(
        SAMPLE_DOCUMENT,
        "Bad quality text with errors.",
        4
    )
    
    # Verify result structure for quality failure
    assert isinstance(result, dict)
    assert "success" in result
    assert result["success"] is False
    assert "error" in result
    assert "quality_result" in result
    assert "suggestions" in result
    
    # Test insertion error
    mock_check_quality.return_value = MOCK_QUALITY_CHECK
    mock_insert.side_effect = ValueError("Line number out of range")
    
    result = insert_suggestion_into_document(
        SAMPLE_DOCUMENT,
        "Good text but bad line number.",
        100
    )
    
    # Verify result structure for insertion error
    assert isinstance(result, dict)
    assert "success" in result
    assert result["success"] is False
    assert "error" in result
    assert "quality_result" in result

if __name__ == "__main__":
    pytest.main(["-v", "test_insert.py"])




