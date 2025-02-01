import json
import os

class JSONFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.directory = os.path.dirname(file_path)

    def _ensure_directory_exists(self):
        """指定されたディレクトリが存在することを確認し、存在しない場合は作成します。"""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def read_json(self):
        """JSONファイルを読み込みます。ファイルが存在しない場合は例外を発生させます。"""
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"JSONデコードエラー: {e}")

    def delete_file(self):
        """JSONファイルを削除します。ファイルが存在しない場合は例外を発生させます。"""
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"ファイルが見つかりません: {self.file_path}")
        os.remove(self.file_path)
    def write_json(self, data):
        """データをJSONファイルに書き込みます。必要に応じてディレクトリを作成します。"""
        self._ensure_directory_exists()
        with open(self.file_path, 'w', encoding='utf-8') as file:
            try:
                json.dump(data, file, indent=4, ensure_ascii=False)
            except TypeError as e:
                raise ValueError(f"JSONエンコードエラー: {e}")

# 使用例
if __name__ == "__main__":
    # ファイルパスを指定してクラスをインスタンス化
    handler = JSONFileHandler('path/to/your/file.json')

    # JSONファイルからの読み込み
    try:
        loaded_data = handler.read_json()
        print("JSONファイルからデータを読み込みました:", loaded_data)
    except (FileNotFoundError, ValueError) as e:
        print(f"読み込みエラー: {e}")

    # JSONファイルの削除
    try:
        handler.delete_file()
        print("JSONファイルを削除しました。")
    except FileNotFoundError as e:
        print(f"削除エラー: {e}")
