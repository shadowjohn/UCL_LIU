%module iadd

#if defined(SWIGJAVASCRIPT)
%rename(addto) operator+=;
#endif

%include attribute.i
class Foo; 
%attributeref(test::Foo, test::A&, AsA);
%attributeref(test::Foo, long, AsLong);


%inline %{
struct B {
	int x;
	B(const int x) : x(x) {}
	
        B& get_me() 
        {
		return *this;
        }
  
	B& operator+=(const B& a) {
		x += a.x;
		return *this;
	}
};



namespace test { 

struct A {
	int x;
	A(const int x) : x(x) {}
	
        A& get_me() 
        {
		return *this;
        }
  
	A operator+=(const A& a) {
		x += a.x;
		return *this;
	}
};


class Foo {
public: 
	Foo(): _a(new A(5)), _n(new long) {}
	~Foo() { delete _a; delete _n; _a = NULL; _n = NULL; }

	A & AsA() const { return *_a; }
	long& AsLong() const { return *_n; }
private: 
	A *_a;
	long *_n;
};
}

%}
