compile:
	@echo "Compiling nylo..."
	@nuitka --python-version=3.6 --recurse-all src/main.py
	@sudo rm -rf main.build
	@sudo mv main.exe nylo

install:
	@echo "Installing nylo..."
	@cd src && sudo python3 setup.py install
	@cd ..
	@sudo cp nylo /usr/bin/nylo
	@sudo mv nylo /usr/local/bin/nylo
	@echo "Finished!"
