import re
import json
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup


def _camel_to_kebab(value: str) -> str:
    out: List[str] = []
    for ch in value:
        if ch.isupper():
            out.append("-")
            out.append(ch.lower())
        else:
            out.append(ch)
    return "".join(out).lstrip("-")


def _mui_slug(component_name: str) -> str:
    # Button -> button, TextField -> text-field, IconButton -> icon-button
    return _camel_to_kebab(component_name).lower()


def _extract_text(element) -> str:
    if element is None:
        return ""
    # Remove code blocks formatting spaces
    return re.sub(r"\s+", " ", element.get_text(separator=" ").strip())


def _parse_props_table(table) -> List[Dict[str, Any]]:
    props: List[Dict[str, Any]] = []
    if table is None:
        return props

    # Identify header indices
    headers = [
        _extract_text(th).lower() for th in table.find_all("th")
    ]
    # Fallback to the first header row only
    if not headers:
        thead = table.find("thead")
        if thead:
            headers = [
                _extract_text(th).lower() for th in thead.find_all("th")
            ]

    def idx(name: str) -> Optional[int]:
        try:
            return headers.index(name)
        except ValueError:
            return None

    idx_name = idx("name")
    idx_type = idx("type")
    idx_default = idx("default")
    # Some pages use "description"; others fold it into name cell
    idx_desc = idx("description")

    tbody = table.find("tbody") or table
    for tr in tbody.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        if not tds:
            continue

        name_txt = _extract_text(tds[idx_name]) if idx_name is not None and idx_name < len(tds) else _extract_text(tds[0])
        type_txt = _extract_text(tds[idx_type]) if idx_type is not None and idx_type < len(tds) else ""
        default_txt = _extract_text(tds[idx_default]) if idx_default is not None and idx_default < len(tds) else ""
        desc_txt = _extract_text(tds[idx_desc]) if idx_desc is not None and idx_desc < len(tds) else ""

        required = False
        # Heuristics: required chip text or suffix
        if re.search(r"required", name_txt, re.I) or re.search(r"required", desc_txt, re.I):
            required = True
        # Clean name (remove required labels, backticks)
        name_txt = re.sub(r"\s*\(required\)\s*", "", name_txt, flags=re.I)
        name_txt = name_txt.strip("`")

        props.append(
            {
                "name": name_txt,
                "type": type_txt or None,
                "default": default_txt or None,
                "required": required,
                "description": desc_txt or None,
            }
        )

    return props


def extract_mui_component(component_name: str) -> Dict[str, Any]:
    """Fetch and parse a MUI v7 component API page and return a JSON-able dict.

    Notes:
    - Network access required. Does not write files; returns data only.
    - Scope: @mui/material.
    """
    slug = _mui_slug(component_name)
    url = f"https://mui.com/material-ui/api/{slug}/"

    resp = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (+AI Migration Tool)",
            "Accept": "text/html,application/xhtml+xml",
        },
        timeout=20,
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")

    # Description: first paragraph under main header
    description = ""
    h1 = soup.find(["h1", "h2"])  # page title
    if h1:
        # Look for next <p>
        p = h1.find_next("p")
        description = _extract_text(p)

    # Find props table: search for a table near a heading containing "Props"
    props: List[Dict[str, Any]] = []
    props_heading = None
    for hdr in soup.find_all(["h2", "h3", "h4"]):
        if re.search(r"\bprops\b", _extract_text(hdr), re.I):
            props_heading = hdr
            break
    if props_heading:
        candidate_table = props_heading.find_next("table")
        props = _parse_props_table(candidate_table)
    else:
        # Fallback: first table with Name/Type headers
        for tbl in soup.find_all("table"):
            header_text = _extract_text(tbl.find("tr"))
            if re.search(r"name", header_text, re.I) and re.search(r"type", header_text, re.I):
                props = _parse_props_table(tbl)
                if props:
                    break

    # Infer events from props starting with on*
    events = []
    for p in props:
        pname = p.get("name", "")
        ptype = (p.get("type") or "").lower()
        if pname.startswith("on") and ("func" in ptype or "function" in ptype):
            events.append({"name": pname, "description": p.get("description")})

    return {
        "name": component_name,
        "import_path": f"@mui/material/{component_name}",
        "description": description or None,
        "props": props,
        "events": events,
        "slots": [],
        "source_url": url,
    }


