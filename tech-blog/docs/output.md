# Change History

## Commit: cdfbba1afd7a0c9e9d065ab292f2ddea3de7bb23
**Author**: raykim
**Date**: 2024-01-13 10:55:58+09:00
**Message**:
```
경로 인식 문제.
상대 경로 -> 절대 경로

```
**Changes**:
```diff
diff --git "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py" "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"
index 707fcfd..414a673 100644
--- "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"	
+++ "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"	
@@ -50,7 +50,7 @@ def check_hyperlinks_in_directory(directory):
     return report
 
 # Replace 'your_directory_path' with the path to the directory you want to check
-directory_path = './input/dev4'
+directory_path = 'C:/Users/khy/Documents/personal/workspace/toolbox/링크 체커/input/dev4/authv4'
 link_report = check_hyperlinks_in_directory(directory_path)
 
 # Print the report
```

## Commit: 728f4fa5ab8e981cd7db66bb2cf65db2bea386a1
**Author**: raykim
**Date**: 2024-01-13 11:33:06+09:00
**Message**:
```
링크 주소 내에 워드프레스 custom variable을 사용하는 링크가 있음. 이를 다시 정상적인 URL 주소로 변환하는 작업 구현

```
**Changes**:
```diff
diff --git "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py" "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"
index 414a673..6ae435c 100644
--- "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"	
+++ "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"	
@@ -3,6 +3,12 @@ import requests
 from bs4 import BeautifulSoup
 from urllib.parse import urljoin
 
+CV_DICT = {"[cgv hive_sdk4_unity_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/Unity3D",
+    "[cgv hive_sdk4_android_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/Android",
+    "[cgv hive_sdk4_ios_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/iOS",
+    "[cgv hive_sdk4_cpp_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/CPP",
+}
+
 def find_html_files(directory):
     """Recursively find all HTML files in the given directory."""
     html_files = []
@@ -12,12 +18,19 @@ def find_html_files(directory):
                 html_files.append(os.path.join(root, file))
     return html_files
 
+def custom_variable_parser(link, replacements=CV_DICT):
+    for target, replacement in replacements.items():
+        if target in link:
+            link = link.replace(target, replacement)
+    return link
+
 def get_hyperlinks(html_file):
     """Extract hyperlinks from an HTML file, excluding image links."""
     with open(html_file, 'r', encoding='utf-8') as file:
         contents = file.read()
         soup = BeautifulSoup(contents, 'html.parser')
         links = [a['href'] for a in soup.find_all('a', href=True) if not a['href'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
+        links = [custom_variable_parser(link) for link in links]
         return links
 
 def check_link_status(url):
```

## Commit: c4a9daedabf54d07f5086d9be64c090b380dc652
**Author**: raykim
**Date**: 2024-01-13 16:03:39+09:00
**Message**:
```
링크 체크를, 웹 링크, 로컬 링크 (로컬 디렉토리에 있는 다른 페이지의 다른 섹션에 있는 앵커로 이동), with-in page 로컬 링크 (현재 페이지의 네임드 앵커로 이동)로 나누어서 실행.
전처리 함수는 웹에서 쓰는 상대 경로를 로컬 기준으로 다시 변동(1뎁스씩 제거)하는 작업 수행.
수정한 상대 경로 처리를 아직 보완해야 함. 불 필요한 로직이 들어간 것으로 보임. 뒤에 "/"가 붙었을 때 처리가 과연 필요한지 체크해야함.

```
**Changes**:
```diff
diff --git "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py" "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"
index 6ae435c..ea01d58 100644
--- "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"	
+++ "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker.py"	
@@ -2,12 +2,14 @@ import os
 import requests
 from bs4 import BeautifulSoup
 from urllib.parse import urljoin
+import re
 
 CV_DICT = {"[cgv hive_sdk4_unity_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/Unity3D",
     "[cgv hive_sdk4_android_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/Android",
     "[cgv hive_sdk4_ios_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/iOS",
     "[cgv hive_sdk4_cpp_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/CPP",
 }
+WEB_DEV_DOC_BASE = "https://developers.withhive.com"
 
 def find_html_files(directory):
     """Recursively find all HTML files in the given directory."""
@@ -33,7 +35,7 @@ def get_hyperlinks(html_file):
         links = [custom_variable_parser(link) for link in links]
         return links
 
-def check_link_status(url):
+def check_web_link_status(url):
     """Check the status of a hyperlink."""
     try:
         response = requests.head(url, allow_redirects=True, timeout=5)
@@ -44,21 +46,113 @@ def check_link_status(url):
     except requests.RequestException:
         return 'Broken'
 
+def check_within_page_link(html_file, relative_link):
+    with open(html_file, 'r', encoding='utf-8') as file:
+        contents = file.read()
+        anchor_pattern = rf'id=(\"|\'){relative_link[1:]}(\"|\')'
+        match = re.search(anchor_pattern, contents)
+        if match:
+            return 'Working'
+        else:
+            return 'Broken'
+
+def check_local_link_status(html_file, relative_link):
+    """Check the status of a local hyperlink."""
+    # 웹 상대 경로를 로컬 상대 경로로 복구, 잘못된 패턴 스크리닝 등 전처리
+    relative_link_orig = pre_process(relative_link)
+    if "#" in relative_link_orig:
+        relative_link_orig, id = relative_link_orig.split("#")
+    else:
+        id = None
+
+    # relative_link (relative_link_orig) 실제값은 2가지 경우가 존재함.
+    # 1. 웹 URL 상의 경로(폴더)
+    # 2. 웹 URL 상의 데이터 (페이지 또는 HTML 파일)
+    # 하지만, relative_link 값으로 이를 구분할 수 없음. 따라서 일단 모든 relative_link는 HTML 파일로 가정하고, .html 확장자를 붙여줌. 경로가 존재하더라도 파일이 존재하지 않으면 Broken으로 처리함.
+    # 단, relative_link 마지막에 "/"이 있으면, 이는 경로로 처리할 수 있음. 이 경우에는 .html 확장자를 붙이지 않음.
+    # 이를 더 낫게 구현하려면 Link라는 클래스를 만들고 경로 or 파일 여부를 Property로 처리해야할 것으로 보임.
+        
+    # relative_link_orig 뒤에 /가 붙어있으면 경로로 취급함. 경로인 경우에는 .html 확장자를 붙이지 않음.
+    if relative_link_orig.endswith('/'):
+        # 예외 처리: relative_link_orig가 경로인데 id가 있을 수는 없으므로, 이런 경우는 바로 Broken 처리
+        if id is not None:
+            return 'Broken'
+        
+        # Convert backslashes to forward slashes for URL formatting
+        html_file = html_file.replace('\\', '/')
+        # Join the directory (as a URL) with the relative link
+        resolved_path = urljoin(f'file://{html_file}', relative_link_orig)
+        local_path = resolved_path.replace('file://', '')
+
+    # relative_link_orig 뒤에 /가 없으므로 파일로 취급해 .html 확장자를 붙임.
+    # 단, /가 없어도 경로일 수 있음. 이 경우는 결국 경로.html이 되어 Broken으로 처리되므로 safe하다고 할 수 있음.
+    else:
+        # Convert backslashes to forward slashes for URL formatting
+        html_file = html_file.replace('\\', '/')
+        # Join the directory (as a URL) with the relative link
+        resolved_path = urljoin(f'file://{html_file}', relative_link_orig)
+        local_path = resolved_path.replace('file://', '')
+        if local_path.endswith('.html'):
+            pass 
+        else:
+            local_path += ".html"
+
+    # 파일 또는 경로가 존재하는지 체크
+    if os.path.exists(local_path):
+        if id is None:
+            return 'Working'
+        else:
+            with open(local_path, 'r', encoding='utf-8') as file:
+                contents = file.read()
+                anchor_pattern = rf'id=(\"|\'){id}(\"|\')'
+                match = re.search(anchor_pattern, contents)
+                if match:
+                    return 'Working'
+                else:
+                    return 'Broken'
+    else:
+        return 'Broken'
+
+def pre_process(relative_link):
+    # 워드프레스에서 쓰는 상대경로 (상위 path로 1단계 올림)를 원래 상대경로로 바꿔줌
+    # 1단계씩 "제거"함.
+    if relative_link.startswith("../../"):
+        return relative_link.replace("../../", "../")
+    elif relative_link.startswith("../"):
+        return relative_link.replace("../", "./")
+    elif relative_link.startswith("./"):
+        return relative_link.replace("./", "")
+    else:
+        raise ValueError("Invalid relative link: " + relative_link + "")
+
 def check_hyperlinks_in_directory(directory):
     """Check all hyperlinks in all HTML files within a directory."""
     html_files = find_html_files(directory)
     report = {}
 
     for html_file in html_files:
-        base_url = 'file://' + html_file
+        # base_url = 'file://' + html_file
         hyperlinks = get_hyperlinks(html_file)
         report[html_file] = []
 
         for link in hyperlinks:
-            # Resolve relative URLs
-            full_url = urljoin(base_url, link)
-            status = check_link_status(full_url)
-            report[html_file].append((link, status))
+            # 웹 링크 체크
+            if link.startswith("http"):
+                status = check_web_link_status(link)
+                report[html_file].append((link, status))
+            elif link.startswith('/?page_id='):
+                link = WEB_DEV_DOC_BASE + link
+                status = check_web_link_status(link)
+                report[html_file].append((link, status))
+            # 로컬 링크 체크
+            elif link.startswith('./') or link.startswith('../'):
+                status = check_local_link_status(html_file, link)
+                report[html_file].append((link, status))
+            elif link.startswith('#'):
+                status = check_within_page_link(html_file, link)
+                report[html_file].append((link, status))
+            else:
+                raise ValueError("Invalid link: " + link + "")
 
     return report
 
```

## Commit: 51fb7fa30d43d918e50311d3b0ecb1b53ea290d6
**Author**: raykim
**Date**: 2024-01-13 20:14:23+09:00
**Message**:
```
링크 체커: 프롬프트 최적화한 다음 코드 다시 요청함.
근데 작동 안 하는 코드이긴 마찬가지임.

```
**Changes**:
```diff
diff --git "a/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker_with_pt_opt.py" "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker_with_pt_opt.py"
new file mode 100644
index 0000000..75b9fbd
--- /dev/null
+++ "b/workspace/toolbox/\353\247\201\355\201\254 \354\262\264\354\273\244/link_checker_with_pt_opt.py"	
@@ -0,0 +1,98 @@
+import os
+import requests
+from bs4 import BeautifulSoup
+from urllib.parse import urljoin, urlparse
+
+CV_DICT = {"[cgv hive_sdk4_unity_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/Unity3D",
+    "[cgv hive_sdk4_android_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/Android",
+    "[cgv hive_sdk4_ios_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/iOS",
+    "[cgv hive_sdk4_cpp_api_ref]":"https://developers.withhive.com/HTML/v4_api_reference/CPP",
+}
+WEB_DEV_DOC_BASE = "https://developers.withhive.com"
+
+def custom_variable_parser(link, replacements=CV_DICT):
+    for target, replacement in replacements.items():
+        if target in link:
+            link = link.replace(target, replacement)
+    return link
+
+def perm_link_parser(link):
+    if link.startswith('/?page_id='):
+        link = WEB_DEV_DOC_BASE + link
+    return link
+
+def pre_process(relative_link):
+    # 워드프레스에서 쓰는 상대경로 (상위 path로 1단계 올림)를 원래 상대경로로 바꿔줌
+    # 1단계씩 "제거"함.
+    if relative_link.startswith("../../"):
+        return relative_link.replace("../../", "../")
+    elif relative_link.startswith("../"):
+        return relative_link.replace("../", "./")
+    elif relative_link.startswith("./"):
+        return relative_link.replace("./", "")
+    else:
+        raise ValueError("Invalid relative link: " + relative_link + "")
+    
+def is_valid_url(url):
+    parsed = urlparse(url)
+    return bool(parsed.netloc) and bool(parsed.scheme)
+
+def get_all_html_files(dir):
+    html_files = []
+    for root, dirs, files in os.walk(dir):
+        for file in files:
+            if file.endswith('.html'):
+                html_files.append(os.path.join(root, file))
+    return html_files
+
+def check_link(url, root):
+    if is_valid_url(url):
+        try:
+            response = requests.head(url, allow_redirects=True)
+            return response.status_code == 200
+        except requests.ConnectionError:
+            return False
+    else:
+        return os.path.exists(os.path.join(root, url))
+
+def find_and_check_links(file):
+    with open(file, 'r', encoding='utf-8') as html_file:
+        soup = BeautifulSoup(html_file, 'html.parser')
+        links = soup.find_all('a', href=True)
+        root = os.path.dirname(file)
+        results = {}
+
+        for link in links:
+            url = link['href']
+            if url.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Skipping image files
+                continue
+            if url.startswith('.'):
+                print(f"Relative link found: {url}")
+                url = pre_process(url)
+            else:
+                url = custom_variable_parser(url)
+                url = perm_link_parser(url)
+            # 이 부분 코드에 문제있음.
+            full_url = urljoin('file:', os.path.abspath(url))
+            link_status = check_link(full_url, root)
+            results[full_url] = link_status
+        return results
+
+def main(directory):
+    html_files = get_all_html_files(directory)
+    all_results = {}
+
+    for file in html_files:
+        all_results[file] = find_and_check_links(file)
+
+    # Reporting the results
+    for file, results in all_results.items():
+        print(f"Results for {file}:")
+        for link, status in results.items():
+            status_text = 'Working' if status else 'Broken or Incorrect'
+            print(f" - {link}: {status_text}")
+
+if __name__ == "__main__":
+    # directory = input("Enter the directory path: ")
+    directory = 'C:/Users/khy/Documents/personal/workspace/toolbox/링크 체커/input/dev4/authv4'
+    main(directory)
```

