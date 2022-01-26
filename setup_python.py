import sys
import os
import subprocess
from subprocess import PIPE, STDOUT
from pathlib import Path
from typing import Any


proc_arg = {
    'shell': True,
    'stdout': PIPE,
    'text': True
}


def _run(*cmd):
    proc = subprocess.run(cmd, **proc_arg, stderr=PIPE)
    return proc.stdout.replace('\n', '')


def _popen(*cmd):
    print(f'$ {" ".join(cmd)}')
    proc = subprocess.Popen(cmd, **proc_arg, stderr=STDOUT)
    while True:
        if line := proc.stdout.readline():
            print(line.replace('\n', ''))
        elif poll := proc.poll() is not None:
            print()
            return poll


def _conf_exit(code, rm=False):
    input('\n処理を終了します。メッセージを確認してEnterを押してください。')
    if rm: os.remove(__file__)
    sys.exit(code)


def _input_yn(msg):
    yn = ''
    while not (yn == 'y' or yn == 'n'):
        yn = input(f'{msg}(y/n): ')
    return {'y': 1, 'n': 0}[yn]


def pip_install(*names):
    _popen('python', '-m', 'pip', 'install', '--upgrade', 'pip')
    for name in names:
        _popen('pip', 'install', name)


def remove_venv():
    if venv_path := _run('pipenv', '--venv'):
        ok = _input_yn(
            '仮想環境が既に存在します。\n'
            f'{venv_path} \n'
            'このフォルダを消去して新しく環境を作成しますか？'
        )
        if not ok: _conf_exit(1)
        _popen('pipenv', '--rm')


def exists_in_cd(tgt):
    cd = Path(_run('cd'))
    if not (cd/tgt).exists():
        print(f'{tgt} が存在しません。カレントディレクトリを確認してください。')
        _conf_exit(1)


def _change_ver(name: str, ver: str) -> None:
    """`pipenv update/install ...`を使用せず、仮想環境の`pip`を直接使ってライブラリのバージョンを変更します。

    Note:
        `Pipfile.lock`で管理できない、環境作成時に用いるセットアップ系ライブラリを指定するための関数。
    """
    print(f'`{name}`のバージョンを{ver}に変更します。')
    _popen('pipenv', 'run', 'python', '-m', 'pip', 'uninstall', '-y', name)
    _popen('pipenv', 'run', 'python', '-m', 'pip', 'install', f'{name}=={ver}')


def is_in_pipfile_lock(lib_name: str) -> bool:
    """ライブラリが`Pipfile.lock`に指定されているかを返す"""
    lock_data = (Path(_run('cd')) / 'Pipfile.lock').read_text(encoding='utf_8')
    return f'"{lib_name}"' in lock_data


def create_venv(setuptools_ver: str = None, wheel_ver: str = None) -> None:
    """`pipenv`を用いて実行ディレクトリ直下に`.venv`フォルダを作りPython仮想環境を作ります。

    Args:
        setuptools_ver (str, optional): 環境作成に用いる`setuptools`のバージョンを指定します。
            デフォルトではローカル環境にある`pipenv`の仕様に依存したバージョンとなります。
        wheel_ver (str, optional): 環境作成に用いる`wheel`のバージョンを指定します。
            デフォルトではローカル環境にある`pipenv`の仕様に依存したバージョンとなります。
    """
    print('仮想環境を作成します。')
    os.environ['PIPENV_VENV_IN_PROJECT'] = 'true'
    print('`.venv`フォルダを作成して`python.exe`や環境セットアップ系ライブラリをインストールします。')
    # `pipenv sync ...`前に`pipenv run ...`することで、ライブラリ依存関係構築の前に
    # `.venv`フォルダを作成してデフォルトの`pip`, `setuptools`, `wheel`をインストールする
    _popen('pipenv', 'run', 'python', '-m', 'pip', 'list')
    if setuptools_ver:
        _change_ver('setuptools', setuptools_ver)
    if wheel_ver:
        _change_ver('wheel', wheel_ver)
    print('`.venv`フォルダに`Pipfile.lock`で指定されているライブラリをインストールします。')
    _popen('pipenv', 'sync', '--dev')
    print('仮想環境の作成が完了しました。')


def main():
    _popen('chcp', '65001')  # 文字コードにより`pipenv`が失敗する可能性があるため指定
    print('Python環境のセットアップを行います…\n')
    pip_install('pipenv')
    remove_venv()
    exists_in_cd('Pipfile.lock')
    if is_in_pipfile_lock('comtypes'):
        # `comtypes`を3系にインストールするために必要なバージョン。詳細は下記参照
        # https://github.com/enthought/comtypes/issues/180#issuecomment-1009586423
        setuptools_ver, wheel_ver = '57.0.0', '0.36.2'
    else:
        setuptools_ver, wheel_ver = None, None
    create_venv(setuptools_ver, wheel_ver)
    _conf_exit(0, True)


if __name__ == "__main__":
    main()
