# tests/test_chronicle.py

import pytest
from chronicle import Chronicle
from lore_types import Perspective, Intention

@pytest.fixture
def chronicle_instance():
    """Provides a default Chronicle instance for testing."""
    config = {"write_to_file": False, "print_to_cmd": True}
    return Chronicle(config=config)

def test_format_for_console_perspective(chronicle_instance):
    """Tests that a Perspective object is correctly formatted for the console."""
    perspective = Perspective(
        owner="TestAgent",
        turn_origin=1,
        content="This is a test perspective.",
        primer="",
        personality="",
        reality_formatted=""
    )
    expected_output = '\nTestAgent perceives: "This is a test perspective...."'
    assert chronicle_instance._format_for_console(perspective) == expected_output

def test_format_for_file_intention(chronicle_instance):
    """Tests that an Intention object is correctly formatted for a markdown file."""
    intention = Intention(
        owner="TestAgent",
        turn_origin=2,
        primer="<ROLE>You are a test agent.</ROLE>",
        formatted_memory="Turn 1: I saw a thing.",
        content="I will now do a thing.",
        prompt="This was the prompt."
    )
    
    output = chronicle_instance._format_for_file(intention, "test.md", "Test Intention")

    # Check for main components
    assert "### Turn: 2 | Test Intention | Owner: TestAgent" in output
    assert "#### Content\nI will now do a thing." in output
    assert "#### Prompt\n```\nThis was the prompt.\n```" in output
    
    # Check for metadata list format
    assert "#### Metadata" in output
    assert "- **primer**:" in output
    assert "- **formatted_memory**:" in output
