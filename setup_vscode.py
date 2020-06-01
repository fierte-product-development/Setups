import sys
import os
import json
from pathlib import Path


SETTINGS = {
    'editor.renderWhitespace': 'boundary',
}


def _conf_exit(code, rm=False):
    input('\n処理を終了します。メッセージを確認してEnterを押してください。')
    if rm: os.remove(__file__)
    sys.exit(code)


def get_vscode_settings():
    user = os.getenv('USERPROFILE')
    if not user:
        print('環境変数 USERPROFILE が見つかりません。')
        _conf_exit(1)
    return Path(user) / 'AppData' / 'Roaming' / 'Code' / 'User' / 'settings.json'


def merge_settings(path):
    if not path.exists(): return SETTINGS
    current_settings = json.loads(path.read_text(encoding='utf-8'))
    return {**current_settings, **SETTINGS}


def write_settings(path, settings):
    data = json.dumps(settings, indent=4, ensure_ascii=False)
    path.write_text(data, encoding='utf-8')


def print_settings(settings):
    print('以下の項目を設定しました。')
    for k, v in settings.items():
        print(f'{k}: {v}')


def main():
    print('VSCodeのセットアップを行います…\n')
    settings_path = get_vscode_settings()
    settings = merge_settings(settings_path)
    write_settings(settings_path, settings)
    print_settings(SETTINGS)
    _conf_exit(0, True)


if __name__ == "__main__":
    main()
