# Setups
環境やエディタのセットアップ用スクリプト。  
必要なものを各プロジェクトのルートに落として起動してください。  
なお全てのスクリプトは終了後に自動で消えるようになっています。

* [setup_pre-commit.py](./setup_pre-commit.py)  
	<必須>  
	Git hooksの発火用スクリプトを./.git/hooksにインストールします。
* [setup_vscode.py](./setup_vscode.py)  
	<必須> ※VS Codeを使用する場合  
	setting.jsonに設定を追加します。おすすめの設定があれば追加するので教えてください
* [setup_python.py](./setup_python.py)  
	<必須> ※Pythonを使用する場合  
	./Pipfile.lockから仮想環境を作成します。./.venvフォルダが生成されます。
