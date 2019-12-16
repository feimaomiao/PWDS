# Change Logs #
- - - -
#### 2019/12/15 04:25 ####
* Changed License.md to my actual name  
<details>
	<summary>Added [wait for input] into funcs.py</summary>
	<p>now it imports a class and prints the color imported  </p>
</details>
<details>
	<summary>Added new file userClass.py</summary>
	<p>pwd.py imports a class from userClass.py</p>
	<p>neater codes  </p>
</details>
<details>
	<summary>Added pwd.py previous class structure into userClass.py</summary>
	<p>pwd.py now only includes prompt and calling class</p>
	<p>neater codes, easier references</p>
</details>
- - - -                   
#### 2019/12/16 01:48 ####
<details>
	<summary>New procedure in login function</summary>
	<p>instantQuit skips ```userInterface.checkbackup()``` function and enhances performance</p>
</details>
<details>
	<summary>Altered pwd.py login process</summary>
	<p>
		```if newuser: {initialise...login }
		else: {login}`
		-->
		`if newuser: {initialise}
		{login}```  
	</p>
</details>
* Added error handling 'instantQuit' in pwd.py  
* New error handling prevents possible flaw while importing backups.