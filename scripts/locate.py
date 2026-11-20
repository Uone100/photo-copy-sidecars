import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat

def linked(path):
    s=path.lstat()
    return stat.S_ISLNK(s.st_mode) or bool(getattr(s,"st_file_attributes",0) & 0x400)

def digest(path):
    before=path.stat()
    with path.open("rb") as f:
        h=hashlib.sha256()
        for data in iter(lambda:f.read(1024*1024),b""):
            h.update(data)
    after=path.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise OSError("File changed during scan")
    return h.hexdigest()

def sidecars(image):
    items=[]
    numbered=re.compile(re.escape(image.stem)+r"_(\d{2,})"+re.escape(image.suffix)+r"\.xmp",re.I)
    for f in image.parent.iterdir():
        if f.suffix.lower()!=".xmp":
            continue
        n=f.name.casefold()
        m=numbered.fullmatch(f.name)
        if n==(image.name+".xmp").casefold(): role="full-name"
        elif n==(image.stem+".xmp").casefold(): role="stem-only"
        elif m: role="darktable-version-"+m[1]
        else: continue
        if linked(f) or not f.is_file():
            raise OSError("Sidecar unavailable for comparison")
        items.append({"role":role,"name":f.name,"sha256":digest(f)})
    return sorted(items,key=lambda x:(x["role"],x["sha256"],x["name"]))

def signature(items):
    return sorted((s["role"],s["sha256"]) for s in items)

def locate(reference,root):
    if not root.is_dir() or not reference.is_file() or linked(reference) or linked(root):
        raise ValueError("Choose a regular reference file and a local directory")
    key=digest(reference)
    size=reference.stat().st_size
    original=sidecars(reference)
    matches=[]
    errors=[]
    def walk_error(e):
        errors.append(str(e))
    for folder,dirs,files in os.walk(root,onerror=walk_error,followlinks=False):
        base=Path(folder)
        for name in list(dirs):
            try:
                if linked(base/name): dirs.remove(name)
            except OSError as exc:
                dirs.remove(name)
                errors.append(str(exc))
        for name in files:
            p=base/name
            try:
                if linked(p) or not p.is_file() or p.stat().st_size!=size or digest(p)!=key:
                    continue
                companions=sidecars(p)
                matches.append({"path":p.relative_to(root).as_posix(),"adjacent_xmp":companions,
                                "same_roles_and_bytes":signature(companions)==signature(original)})
            except OSError as exc:
                errors.append(str(exc))
    return {"reference_sha256":key,"reference_xmp":original,"matches":sorted(matches,key=lambda x:x["path"]),
            "scan_errors":errors}

if __name__=="__main__":
    p=argparse.ArgumentParser(description="Find exact copies and compare local XMP variants")
    p.add_argument("reference",type=Path)
    p.add_argument("folder",type=Path)
    a=p.parse_args()
    try:
        result=locate(a.reference,a.folder)
    except (OSError,ValueError) as exc:
        p.exit(2,f"{exc}\n")
    print(json.dumps(result,ensure_ascii=True,indent=2))
    raise SystemExit(1 if result["scan_errors"] else 0)
