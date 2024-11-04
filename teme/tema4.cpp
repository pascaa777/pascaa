#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

class Student {
    string nume, spec;
    int an;
    float media;
public:
    Student(string nume, string spec, int an, float media)
        : nume(nume), spec(spec), an(an), media(media) {}

    static bool compNume(Student *s1, Student *s2) { return s1->nume > s2->nume; }
    static bool compMedia(Student *s1, Student *s2) { return s1->media < s2->media; }

    static void afiseaza(Student *studenti[], int n) {
        for (int i = 0; i < n; i++) {
            cout << '\t' << studenti[i]->nume << ", " << studenti[i]->spec << ", "
                 << studenti[i]->an << ", " << studenti[i]->media << '\n';
        }
    }
};

class TabStudenti {
    Student **studenti;
    int n;
public:
    TabStudenti(int n): n(n) {
        studenti = new Student*[n];
    }

    void citesteStudenti(ifstream &intrare) {
        string temp;
        int i = 0;
        while (intrare >> temp && i < n) {
            stringstream linie(temp);
            string nume, spec;
            int an;
            float media;

            getline(linie, nume, ',');
            getline(linie, temp, ',');
            nume += " " + temp;
            getline(linie, spec, ',');
            getline(linie, temp, ',');
            an = stoi(temp);
            getline(linie, temp, ',');
            media = stof(temp);

            studenti[i++] = new Student(nume, spec, an, media);
        }
    }

    void afiseazaStudenti() {
        Student::afiseaza(studenti, n);
    }

    void sorteaza(bool (*comparator)(Student*, Student*)) {
        quickSort(studenti, 0, n - 1, comparator);
    }

    ~TabStudenti() {
        for (int i = 0; i < n; i++)
            delete studenti[i];
        delete[] studenti;
    }

private:
    void quickSort(Student* arr[], int low, int high, bool (*comparator)(Student*, Student*)) {
        if (low < high) {
            int pi = partition(arr, low, high, comparator);
            quickSort(arr, low, pi - 1, comparator);
            quickSort(arr, pi + 1, high, comparator);
        }
    }

    int partition(Student* arr[], int low, int high, bool (*comparator)(Student*, Student*)) {
        Student* pivot = arr[high];
        int i = (low - 1);

        for (int j = low; j <= high - 1; j++) {
            if (comparator(arr[j], pivot)) {
                i++;
                swap(arr[i], arr[j]);
            }
        }
        swap(arr[i + 1], arr[high]);
        return (i + 1);
    }
};

int main() {
    ifstream intrare("studenti.txt");
    if (intrare.fail()) {
        cout << "Eroare deschidere fisier";
        return 1;
    }

    int n = 0;
    string temp;
    while (getline(intrare, temp))
        n++;

    intrare.clear();
    intrare.seekg(0, ios::beg);

    TabStudenti tabStudenti(n);
    tabStudenti.citesteStudenti(intrare);
    intrare.close();

    cout << "Studenti inainte de sortare:\n";
    tabStudenti.afiseazaStudenti();

    tabStudenti.sorteaza(Student::compMedia); // Sorteaza dupa medie, de exemplu

    cout << "\nStudenti dupa sortare:\n";
    tabStudenti.afiseazaStudenti();

    return 0;
}

