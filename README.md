# md5crawler

An application to find duplicate files within a given directory using MD5 hash keys.  

Language: Python 3 

## How do I run the program? 

Python 3 must be installed on your system to run this application.  

No external libraries are required, simply configure the application parameters detailed below and run the application as follows: 

python3 md5crawler.py 

## How do I change the application settings? 

Open md5crawler.py in a text editor and search for the following lines: 

```python
#####PARAMS#####  

# Specify the parameters for your search. You'll probably want to change these.  
search_dir = '/home/user/' 
csv_out =  open('/home/user/MD5Out.csv', 'w') 
################ 
```
You can safely change these parameters as needed, just remember to keep your changes wrapped in quotation marks. 
To change the location where the application will check for duplicate MD5 hashes, change the ```search_dir``` variable like the example below: 
```python
search_dir = '/home/user/search' 
```
Similarly, you can change the location where the output report is saved by changing the ```csv_out``` variable as below. Ensure that you only change the file path. Replacing the ,'w') section will break your search. 
```python
csv_out =  open('/home/user/MD5Out.csv', 'w') 
```
## Why use an MD5? Can't we just find duplicate file names? 

Files that share a file name may not be identical.  
As an example, you may have multiple versions of the same file stored in separate folders. These files are not duplicates, they are different working versions of the same file. The internal structure of the files are different to one another.  
Generating an MD5 for each file lets us find files that have an identical internal structure, even if they have a different file name.  

## Is it possible for 2 or more files to have an identical MD5? 
Yes, there is a chance that files may share an MD5 even if they are totally different internally.  
The chances of this happening however, are 0.000000000000000000000000000000000000002938735877055718769921841343055614194546663891. 
Just for some perspective, the chance of the earth getting hit by a 15km asteroid is 0.00000002. 
We can therefore be pretty certain that there will be no MD5 collisions between your files. If there is, consider buying a lottery ticket.  

## Does this program delete the duplicate files? 

Certainly not. It simply creates a CSV file that reports on which files share an MD5 hash.  
The idea of the program is to help you find duplicate files, not to take a wild guess at deleting your data :).  

## I tried running the program, but it's so slow! Is there a way to speed it up? 

Unfortunately not. Generating an MD5 for every file can be a time consuming and intensive process.  
The application is multi-threaded, with the MD5 creation process taking place on a maximum of 10 CPU threads.  
Most of the time however, the main bottleneck is the performance of your device's storage device. Running the script on a solid-state drive will give you much better results than a spinning hard drive.  
