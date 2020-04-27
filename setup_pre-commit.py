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


def pip_install(*names):
    _popen('python', '-m', 'pip', 'install', '--upgrade', 'pip')
    for name in names:
        _popen('pip', 'install', name)


def exists_in_cd(tgt):
    cd = Path(_run('cd'))
    if not (cd/tgt).exists():
        print(f'{tgt} が存在しません。カレントディレクトリを確認してください。')
        _conf_exit(1)


def install_pre_commit():
    print('.git/hooks に commit-msg ファイルを作成します。')
    _popen('pre-commit', 'install', '-t', 'commit-msg')


def main():
    print('pre-commitのセットアップを行います…\n')
    pip_install('pre-commit')
    exists_in_cd('.git')
    install_pre_commit()
    _conf_exit(0, True)


if __name__ == "__main__":
    main()
