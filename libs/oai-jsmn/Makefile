# You can put your build options here
-include config.mk

jsmnlib = libjsmn.a
PREFIX = /usr/local


all: libjsmn.a 

libjsmn.a: jsmn.o
	$(AR) rc $@ $^

%.o: %.c jsmn.h
	$(CC) -c $(CFLAGS) $< -o $@

test: test_default test_strict test_links test_strict_links
test_default: test/tests.c
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o test/$@
	./test/$@
test_strict: test/tests.c
	$(CC) -DJSMN_STRICT=1 $(CFLAGS) $(LDFLAGS) $< -o test/$@
	./test/$@
test_links: test/tests.c
	$(CC) -DJSMN_PARENT_LINKS=1 $(CFLAGS) $(LDFLAGS) $< -o test/$@
	./test/$@
test_strict_links: test/tests.c
	$(CC) -DJSMN_STRICT=1 -DJSMN_PARENT_LINKS=1 $(CFLAGS) $(LDFLAGS) $< -o test/$@
	./test/$@

jsmn_test.o: jsmn_test.c libjsmn.a

example: 
	gcc example.c -o example -ljsmn

jsondump: example/jsondump.o libjsmn.a
	$(CC) $(LDFLAGS) $^ -o $@

.PHONY: install
install:
	mkdir -p $(PREFIX)/lib
	mkdir -p $(PREFIX)/include
	cp $(jsmnlib) $(PREFIX)/lib/$(jsmnlib)
	cp jsmn.h $(PREFIX)/include/

.PHONY: uninstall
uninstall:
	rm -f $(PREFIX)/lib/$(jsmnlib)
	rm -f $(PREFIX)/include/jsmn.h

clean:
	rm -f *.o example/*.o
	rm -f *.a *.so
	rm -f simple_example
	rm -f jsondump

.PHONY: all clean test example

