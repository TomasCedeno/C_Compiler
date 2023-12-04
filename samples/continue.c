int main() {
	int i = 0;
	int a = 0;

	while (i < 10) {
		if (i == 5) {
			i = 11;
			continue;
		}

		i++;
	}

	return i;
}
