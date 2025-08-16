#!/usr/bin/env python3
"""
Resume Keyword Matcher (offline)
Usage:
  python main.py --file job.txt --input "===RESUME===\\n<resume text>"
Or provide job and resume in a single file separated by a line '===RESUME==='
"""
import argparse, requests, os, sys

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = "llama3.2:4b"
TIMEOUT = 300

def run_llama(prompt):
    r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response","").strip()

def build_prompt(combined_text):
    return (
        "You are a recruiter assistant. Compare the JOB description to the RESUME.\n"
        "Output:\n- Match Score: 0-100\n- Missing critical keywords: comma list\n- Top 3 suggestions to improve resume (bullet list)\n\n"
        f"{combined_text}\n\nEnsure output is concise."
    )

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f", help="Path with job + '===RESUME===' + resume OR file with only job (use --input to pass resume)")
    p.add_argument("--input", "-i", help="Inline content or resume prefixed by '===RESUME==='")
    args = p.parse_args()
    content = args.input or ""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                content = (content + "\n" if content else "") + fh.read()
        except Exception as e:
            print("Error:", e, file=sys.stderr); sys.exit(1)
    if "===RESUME===" not in content:
        print("Please include job and resume separated by a line '===RESUME===' or pass both via --input", file=sys.stderr); sys.exit(1)
    print(run_llama(build_prompt(content)))

if __name__ == "__main__":
    main()
