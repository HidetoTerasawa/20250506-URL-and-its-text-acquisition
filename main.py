# 指定したURLのアンカーに設定してあるURLを取得し、各ページのテキストを抽出してマークダウン形式で保存するスクリプト

import requests  # HTTPリクエストを送信するためのライブラリ
from bs4 import BeautifulSoup  # HTML解析を行うためのライブラリ
from urllib.parse import urljoin, urlparse, urlunparse  # URL操作のためのユーティリティ

def remove_short_sections(file_path, min_lines=5):
    """
    マークダウンファイル内で、指定した行数未満のセクションを削除する関数。

    この関数は、マークダウンファイルを読み込み、各セクション（`# URL` で始まる部分）をスキャンします。
    セクション内の行数が `min_lines` 未満の場合、そのセクションを削除します。
    最終的に、条件を満たすセクションのみをファイルに書き戻します。

    Args:
        file_path (str): 処理対象のファイルパス。
        min_lines (int): セクション内の最小行数（これ未満のセクションを削除）。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        filtered_lines = []
        current_section = []
        for line in lines:
            if line.startswith("# "):  # 新しいセクションの開始
                # 現在のセクションが条件を満たしている場合のみ保存
                if len(current_section) >= min_lines:
                    filtered_lines.extend(current_section)
                current_section = [line]  # 新しいセクションを開始
            else:
                current_section.append(line)

        # 最後のセクションをチェック
        if len(current_section) >= min_lines:
            filtered_lines.extend(current_section)

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(filtered_lines)

        print(f"Short sections removed from {file_path}")
    except IOError as e:
        print(f"Error processing file {file_path}: {e}")

def remove_duplicate_lines(file_path):
    """
    マークダウンファイル内の同じ文字列を含む行を削除する関数。

    この関数は、マークダウンファイルを読み込み、重複する行を削除します。
    空行や重複行をスキップし、ユニークな行のみをファイルに書き戻します。

    Args:
        file_path (str): 処理対象のファイルパス。
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        seen = set()
        unique_lines = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and stripped_line not in seen:
                unique_lines.append(line)
                seen.add(stripped_line)

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(unique_lines)

        print(f"Duplicate lines removed from {file_path}")
    except IOError as e:
        print(f"Error processing file {file_path}: {e}")

def extract_urls_from_html(page_url):
    """
    指定したページのHTMLからアンカータグのURLを取得する関数。

    この関数は、指定されたURLのHTMLを取得し、すべてのアンカータグ（`<a>`）の `href` 属性を抽出します。
    抽出されたURLは絶対URLに変換され、フラグメント（`#`以降）を削除します。
    最終的に、正規化されたURLのリストを返します。

    Args:
        page_url (str): 対象のページURL。

    Returns:
        list: ページ内のすべてのアンカータグの絶対URL。
    """
    try:
        response = requests.get(page_url, timeout=5)
        if response.status_code != 200:
            print(f"Failed to fetch page: {page_url} (Status code: {response.status_code})")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        urls = [urljoin(page_url, a.get("href")) for a in soup.find_all("a", href=True)]

        # フラグメント (#以降) を削除し、末尾のスラッシュを統一
        normalized_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            normalized_url = urlunparse(parsed_url._replace(fragment=""))

            # 末尾のスラッシュを削除
            if normalized_url.endswith('/'):
                normalized_url = normalized_url[:-1]

            normalized_urls.append(normalized_url)

        return normalized_urls
    except requests.RequestException as e:
        print(f"Error fetching page: {page_url} ({e})")
        return []

def extract_text_from_url(url, seen_texts, seen_tags):
    """
    指定したURLのページからテキストを抽出する関数。

    この関数は、指定されたURLのHTMLを取得し、ページ内のすべてのテキストを抽出します。
    抽出されたテキストは空行を削除し、整形された文字列として返されます。

    Args:
        url (str): 対象のURL。
        seen_texts (set): 既に抽出されたテキストのセット。（未使用）
        seen_tags (set): 既に抽出されたタグのテキストのセット。（未使用）

    Returns:
        str: ページ内のテキスト。
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"Failed to fetch page: {url} (Status code: {response.status_code})")
            return ""

        soup = BeautifulSoup(response.content, "html.parser")
        # ページ内のテキストを抽出
        text = soup.get_text(separator="\n").strip()

        # 空行を削除
        lines = [line for line in text.splitlines() if line.strip()]
        cleaned_text = "\n".join(lines)

        return cleaned_text
    except requests.RequestException as e:
        print(f"Error fetching page: {url} ({e})")
        return ""

def save_texts_to_markdown(urls, output_file):
    """
    URLリストからテキストを抽出し、指定のマークダウン形式でファイルに保存する関数。

    この関数は、指定されたURLリストを順に処理し、各URLのテキストを抽出します。
    抽出されたテキストは、マークダウン形式でファイルに保存されます。
    各URLは `# URL` の形式でセクションとして記録されます。

    Args:
        urls (list): 処理対象のURLリスト。
        output_file (str): 出力先のファイルパス。
    """
    seen_texts = set()  # 既に抽出されたテキストを記録するセット
    seen_tags = set()   # 既に抽出されたタグのテキストを記録するセット
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for url in urls:
                print(f"Processing URL: {url}")
                text = extract_text_from_url(url, seen_texts, seen_tags)
                if text:  # テキストが空でない場合のみ書き込む
                    file.write(f"# {url}\n")
                    file.write(f"{text}\n\n")  # URLごとに改行を追加
        print(f"Markdown file has been saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")

def main():
    """
    スクリプトのエントリーポイント。

    この関数は、指定されたURLからリンクを抽出し、各リンク先のテキストを取得します。
    取得したテキストはマークダウン形式で保存され、重複行や短いセクションが削除されます。
    """
    page_url = ""
    print(f"Fetching URLs from {page_url}...")

    # HTML内のアンカータグからURLを取得
    urls = extract_urls_from_html(page_url)

    # 重複を削除
    unique_urls = list(set(urls))
    unique_urls.sort()  # ソートして見やすくする（任意）

    print("Extracted URLs:")
    print("\n".join(unique_urls))

    # URLからテキストを抽出してマークダウン形式で保存
    markdown_output_file = "urls_with_texts.md"
    save_texts_to_markdown(unique_urls, markdown_output_file)

    # 重複行を削除
    remove_duplicate_lines(markdown_output_file)

    # 5行未満のセクションを削除
    remove_short_sections(markdown_output_file, min_lines=5)

if __name__ == "__main__":
    main()
