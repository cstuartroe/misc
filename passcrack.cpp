#include <stdio.h>
#include <iostream>

using namespace std;

class Passcracker {
private:
	int length, state;
	bool first;
	Passcracker *child;
	string finished() {
		return "$";
	}
	void newChild() {
		child = new Passcracker(length-1);
	}
	string useChild() {
		string child_out = child->next();
		if (child_out == "$") {
			state++;
			if (state == Passcracker::passchars.length()) { return finished(); }
			else {
				newChild();
				child_out = child->next();
			}
		}
		return string(1,Passcracker::passchars.at(state)) + child_out;
	}
public:
	static string passchars;
	Passcracker(int _length) {
		length = _length;
		state = 0;
		first = true;
	}
	string next() {
		if (first) {
			if (state == Passcracker::passchars.length()) {
				if (length > 1) {
					state = 0;
					first = false;
					newChild();					
					return useChild();
				} else {
					return finished();
				}
			} else {
				string out = string(1,Passcracker::passchars.at(state));
				state++;
				return out;
			}
		} else {
			if (state == Passcracker::passchars.length()) {
				throw runtime_error("How did this happen?");
			} else {
				return useChild();
			}
		}
	}
	int getState() { return state; }
	int getLength() { return length; }
	~Passcracker() { delete child; }
};

int main(int argc, char *argv[]) {
	if (argc == 1) {
		printf("Please provide a password");
		exit (EXIT_FAILURE);
	} else {
		string password = argv[1];
		Passcracker p = Passcracker(password.length());
		string r = p.next();
		while (r != "$") {
			if (password == r) {
				printf("%s",r.c_str());
				exit (EXIT_SUCCESS);
			}
			r = p.next();
		}
	}
}

string Passcracker::passchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";