# builder.py for IGM
I lost the plot. I made an IGM compiler.
The only compiler for Idle Game Maker that has ever (and should ever) exist.
## Premise
I have a problem (well, will have a problem very soon). I have an game I plan to make that involves and excessive excrutiating amount of copy-pasting with minor variations. And that is quite literally the most mind-numbing thing I could do and something I don't want to do.
So, I made a python script for it. builder.py will hopefully be to be a wildly versatile and useful tool to solve that very specific issue.
## Plans
I put it in the comments of the python file. Probably.
## How to start?
First, create any json, anywhere. (but I reccomend creating a build.json in the same folder you have builder.py). Them strucure your json to have the following:
- (optional) a version key: value (kv) pair that specifies the version of builder.py you're using. Mostly used by builder.py to ensure compatibility with things it generated itself.
- (optional) an array named export that specifies where you export your file with two kv pairs: one for your directory (dir) which can be set to cwd to refer to the current working directory (the folder you're in!), and one for your file name (file) which can be set to the name of the file you want to export (extension included!)
- an array named order which specifies the order you put your items (lines) in. the keys are the number of the block that you're writing, and the value is another array! (yay..) with two kv pairs itself. one is for the title (or key, like thingKeys!) of the block, and the other is another array with the key "rept".
- said array is where you specify repetitions! you have two options (in the form a kv pair with key "mode") right now, line (which gives you an x that increases by 1 by each iteration of your block) and dot (which is like line but without giving you an x). and there's another kv pair specifying the size of the loop, with key "size"
- finally, go back to the beginning and put an array named "items", which has arrays- labelled by their block key, with individual lines in the form of kv pairs similar to the ordering of the order array.
OR just use the build.json file in the repo as a template. Your call.
