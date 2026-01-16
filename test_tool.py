from tools import AntigravityBrowserTool

def test_browser():
    print("Initializing Browser Tool...")
    tool = AntigravityBrowserTool()
    print("Running Search Query...")
    # Test with a known safe URL to avoid search engine block inconsistency during automated test
    result = tool._run("https://example.com") 
    print("Result length:", len(result))
    if "Example Domain" in result:
        print("SUCCESS: Browser tool fetched content.")
    else:
        print("FAILURE: Browser tool content mismatch.")
        print(result[:200])

if __name__ == "__main__":
    test_browser()
