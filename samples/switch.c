int main() {
	int i = 5;

	switch(i) {
		case 1: {
			i = 2;
			break;
		}
		case 5: {
			i = 22;
			break;
		}
		case 10: {
			i = 11;
			break;
		}
	}

	return i;
}
