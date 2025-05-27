#!/usr/bin/env python3
"""
Simple runner script for GitHub Repository Analyzer
Prompts for GitHub token securely and runs the analysis
"""

import getpass
import os
from github_repo_analyzer import quick_analyze_modus_wc


def main():
    print("🔍 Modus WC 2.0 Repository Analyzer")
    print("=" * 50)

    # Get GitHub token securely
    token = getpass.getpass("Enter your GitHub Personal Access Token: ")

    if not token or len(token) < 10:
        print("❌ Invalid token. Please provide a valid GitHub Personal Access Token.")
        print("Get one from: https://github.com/settings/tokens")
        return

    print("\n🚀 Starting analysis of trimble-oss/modus-wc-2.0...")
    print("This may take a few minutes depending on repository size.")
    print("=" * 50)

    try:
        # Run the analysis
        results = quick_analyze_modus_wc(
            token=token,
            include_prs=True,  # Include pull requests
            skip_dependency_prs=True,  # Skip dependency PRs
            save_file=True,  # Save to JSON file
        )

        if results:
            print("\n✅ Analysis completed successfully!")

            # Show summary stats
            total_issues = len(results["issues"])
            total_prs = len(results.get("pull_requests", []))
            total_comments = (
                results["analysis_metadata"]["total_issue_comments"]
                + results["analysis_metadata"]["total_pr_review_comments"]
            )

            print(f"\n📊 Summary:")
            print(f"   Issues analyzed: {total_issues:,}")
            print(f"   Pull requests analyzed: {total_prs:,}")
            print(f"   Total comments collected: {total_comments:,}")
            print(
                f"   Dependency PRs skipped: {results['analysis_metadata']['skipped_dependency_prs']:,}"
            )

            # Show file location
            repo_name = results["repository"]["name"]
            timestamp = results["analysis_metadata"]["analyzed_at"][:19].replace(
                ":", "-"
            )
            expected_filename = f"trimble-oss_{repo_name}_analysis_{timestamp.replace('-', '').replace('T', '_')}.json"

            print(f"\n💾 Data saved to JSON file (check current directory)")
            print(f"   Look for files matching: *{repo_name}_analysis_*.json")

            return results
        else:
            print("❌ Analysis failed. Please check your token and try again.")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("Make sure your GitHub token has the necessary permissions.")


if __name__ == "__main__":
    main()
