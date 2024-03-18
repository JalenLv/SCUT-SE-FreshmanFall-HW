#include <iostream>
using namespace std;

char c[100];	//用于保存字符集合

void passgen_v1(int n, char c[], int len)
{
	if (len == 0)
	{
		cout << endl;
		return;
	}

	for (int i = 0; i < n; i++)
	{
		cout << c[i];
		passgen_v1(n, c, len - 1);
	}
}

char ans[100];	//用于保存前若干层递归生成的结果
int cnt = 0;
void passgen_v2(int n, char c[], int len, int LEN_remain)
{
	if (LEN_remain == 0)
	{
		cnt++;
		cout << cnt << "\t";

		for (int i = 0; i < len; i++)
			cout << ans[i];
		
		cout << endl;
		return;
	}

	for (int i = 0; i < n; i++)
	{
		ans[len - LEN_remain] = c[i];
		passgen_v2(n, c, len, LEN_remain - 1);
	}
}

int main()
{
	int n;
	cin >> n;

	for (int i = 0; i < n; i++)
		cin >> c[i];

	int len;
	cin >> len;

	cout << endl << "passgen_v1:" << endl;
	passgen_v1(n, c, len);
	cout << endl;

//	cout << endl << "passgen_v2:" << endl;
//	passgen_v2(n, c, len, len);

	cout << "INDEX" << "\t" << "PASSWORD" << endl;
	for (int i = 1; i <= len; i++)
		passgen_v2(n, c, i, i);
	cout << "Total: " << cnt;

	return 0;
}