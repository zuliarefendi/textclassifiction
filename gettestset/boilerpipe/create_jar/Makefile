#to generate getwebcontent.jar
.PHONY: test_getwebcontent

test_getwebcontent: getwebcontent.jar
	echo "create getwebcontent.jar" 
	java -cp '.:../boilerpipe-1.2.0.jar:../lib/*' Getwebcontent "http://espn.go.com/blog/new-york/jets/post/_/id/21881/slauson-still-thinks-about-cushing-hit"

getwebcontent.jar: Getwebcontent.class
	jar -cf $@ $<

%.class: %.java
	javac -cp '.:../boilerpipe-1.2.0.jar:../lib/*' $<

clean:
	rm -rf getwebcontent.jar Getwebcontent.class
