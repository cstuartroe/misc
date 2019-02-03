#include <iostream>
#include <math.h>

using namespace std;

struct node {
	int data;
	node *next;
};

class list {
	private:
	node *head, *tail;
	public:
	list() {
		head = NULL;
		tail = NULL;
	}
	void append(int value) {
		node *temp = new node;
		temp -> data = value;
		temp -> next = NULL;
		if (head == NULL) {
			head = temp;
			tail = temp;
			temp = NULL;
		} else {
			tail -> next = temp;
			tail = temp;
		}
	}
	void display() {
        node *temp = new node;
        temp = head;
        while (temp != NULL) {
            cout << (temp -> data);
            cout << (" ");
            temp = temp -> next;
        }
        cout << endl;
	}
	node* getHead() {
		return head;
	}
};

list* powersupto(int n) {
	int primes [12] = {2,3,5,7,11,13,17,19,23,29,31,37};
	list *out = new list;

	for(int i = 0; i < 12; i++) {
		int p = primes[i];
		int exp = 1;
		while (pow(p,exp) <= n) {
			out->append(pow(p,exp));
			exp++;
		}
	}

	return out;
}

int main()
{
	node *ps = powersupto(10000000)->getHead();
	while (ps != NULL) {
		node *temp = ps -> next;
		while (temp != NULL) {
			float r = (float) (ps->data)/(temp->data);
			if((r >= .99) && (r <= 1.01)) {
				cout << ps->data << " " << temp->data << " " << r << endl;
			}
			temp = temp->next;
		}
		ps = ps -> next;
	}
}
