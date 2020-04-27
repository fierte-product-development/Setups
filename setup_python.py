import sys
import os
import subprocess
from subprocess import PIPE, STDOUT
from pathlib import Path


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


def create_venv():
    print('.venv フォルダを作成します。')
    os.environ['PIPENV_VENV_IN_PROJECT'] = 'true'
    _popen('pipenv', 'sync', '--dev')


def main():
    print('Python環境のセットアップを行います…\n')
    pip_install('pipenv')
    remove_venv()
    exists_in_cd('Pipfile.lock')
    create_venv()
    _conf_exit(0, True)


if __name__ == "__main__":
    main()
