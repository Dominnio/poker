#include <iostream>
#include <cstring>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <unistd.h>

enum symbol{
    two = 0,
    three = 1,
    four = 2,
    five = 3,
    six = 4,
    seven = 5,
    eight = 6,
    nine = 7,
    ten = 8,
    jack = 9,
    queen = 10,
    king = 11,
    ace = 12
};

enum color{
    club = 0,
    diamond = 1,
    heart = 2,
    spade = 3
};

class Card {
public:
    bool operator==(const Card &other) { return symbol == other.symbol; }

    bool operator!=(const Card &other) { return symbol != other.symbol; }

    bool operator<=(const Card &other) { return symbol <= other.symbol; }

    bool operator>=(const Card &other) { return symbol >= other.symbol; }

    bool operator<(const Card &other) { return symbol < other.symbol; }

    bool operator>(const Card &other) { return symbol > other.symbol; }

    Card(int s, int c) : symbol(s), color(c) {}

    int get_color() const { return color; }

    int get_symbol() const { return symbol; }

    void set_color(int c) { color = c; }

    void set_symbol(int s) { symbol = s; }

private:
    int symbol;
    int color;
};

std::ostream &operator<<(std::ostream &output, const Card &card) {
    std::string c;
    switch (card.get_color()) {
        case 0:
            c = "\u2663";
            break;
        case 1:
            c = "\u2666";
            break;
        case 2:
            c = "\u2665";
            break;
        default:
            c = "\u2660";
            break;
    }
    char s;
    switch (card.get_symbol()) {
        case 12:
            s = 'A';
            break;
        case 11:
            s = 'K';
            break;
        case 10:
            s = 'Q';
            break;
        case 9:
            s = 'J';
            break;
        case 8:
            s = 'T';
            break;
        default:
            s = (char) (card.get_symbol() + 50);
            break;
    }
    return output << s << c;
}

class Set {
public:
    Set(std::vector<Card> c) : cards(c) {
        strength = 0;
        check();
    }

    int compare(const Set &other) {
        if (strength > other.get_strength())
            return 1;
        if (strength < other.get_strength())
            return -1;
        for (int i = 0; i < 5; ++i) {
            if (layout[i] > other.get_layout()[i])
                return i + 2;
            if (layout[i] < other.get_layout()[i])
                return -i - 2;
        }
        return 0;
    }

    void print() {
        for (auto i = cards.begin(); i < cards.end(); i++)
            std::cout << *i << " ";
        std::cout << "\n";
        std::cout << "\n";

        for (auto i = col.begin(); i < col.end(); i++) {
            if ((*i).size() == 0)
                continue;
            for (auto j = (*i).begin(); j < (*i).end(); j++) {
                std::cout << *j << " ";
            }
            std::cout << "\n";
        }
        std::cout << "\n";

        for (auto i = seq.begin(); i < seq.end(); i++) {
            for (auto j = (*i).begin(); j < (*i).end(); j++)
                std::cout << *j << " ";
            std::cout << "\n";
        }
        std::cout << "\n";

    }

    int get_strength() const { return strength; }

    std::vector<Card> get_layout() const { return layout; }

private:
    void set_seq() {
        std::vector<Card> e;
        e.push_back(cards[0]);
        for (auto i = cards.begin(); i < cards.end(); i++) {
            if (*i == *(i + 1)) {
                e.push_back(*(i + 1));
            } else {
                seq.push_back(e);
                e.erase(e.begin(),e.end());
                e.push_back(*(i + 1));
            }
        }
    }

    void set_col() {
        std::vector<Card> s;
        std::vector<Card> c;
        std::vector<Card> h;
        std::vector<Card> d;
        col.push_back(c);
        col.push_back(d);
        col.push_back(h);
        col.push_back(s);
        for (auto i = cards.begin(); i < cards.end(); i++) {
            col[i->get_color()].push_back(*i);
        }
    }

    void check_two_pair(){
        for (unsigned i = 0; i < seq.size(); i++){
            if((seq[i]).size() == 2){
                layout = seq[i];
                seq.erase(seq.begin() + i);
                for (unsigned j = 0; j < seq.size(); j++){
                    if((seq[j]).size() == 2){
                        layout.push_back(seq[j][0]);
                        layout.push_back(seq[j][1]);
                        seq.erase(seq.begin() + j);
                        layout.push_back(seq[0][0]);
                        strength = 3;
                        return;
                    }
                }
                layout.push_back(seq[0][0]);
                layout.push_back(seq[1][0]);
                layout.push_back(seq[2][0]);
                strength = 2;
                return;
            }
        }
        layout.push_back(seq[0][0]);
        layout.push_back(seq[1][0]);
        layout.push_back(seq[2][0]);
        layout.push_back(seq[3][0]);
        layout.push_back(seq[4][0]);
        strength = 1;
        return;
    }

    void check_three(){
        for (unsigned i = 0; i < seq.size(); i++){
            if((seq[i]).size() == 3){
                layout = seq[i];
                seq.erase(seq.begin() + i);
                layout.push_back(seq[0][0]);
                layout.push_back(seq[0][1]);
                strength = 4;
                return;
            }
        }
        check_two_pair();
        return;
    }

    void check_straight(){
        layout.push_back(seq[0][0]);
        for(auto i = seq.begin() + 1; i < seq.end(); i++){
            if((*i)[0].get_symbol() == (*(i-1))[0].get_symbol() - 1) {
                layout.push_back((*i)[0]);
                if(layout.size() == 5){
                    strength = 5;
                    return;
                }
            } else{
                layout.clear();
                layout.push_back((*i)[0]);
            }
        }
        if(layout.size() == 4 and layout[0].get_symbol() == 3 and seq[0][0].get_symbol() == 12) {
            layout.push_back(seq[0][0]);
            strength = 5;
            return;
        }
        check_three();
        return;
    }

    void check_flush(){
        for (auto i = col.begin(); i < col.end(); i++) {
            if((*i).size() >=5){
                (*i).erase((*i).begin() + 5, (*i).end());
                layout = (*i);
                strength = 6;
                return;
            }
        }
        check_straight();
        return;
    }

    void check_full_house(){
        for (unsigned i = 0; i < seq.size(); i++){
            if((seq[i]).size() == 3){
                layout = seq[i];
                for (unsigned j = 0; j < seq.size(); j++){
                    if(seq[j].size() >=2 and seq[j][0].get_symbol() != layout[0].get_symbol()){
                        layout.push_back(seq[j][0]);
                        layout.push_back(seq[j][1]);
                        strength = 7;
                        return;
                    }
                }
            }
        }
        check_flush();
        return;
    }

    void check_quads(){
        for (unsigned i = 0; i < seq.size(); i++){
            if((seq[i]).size() == 4){
                layout = seq[i];
                seq.erase(seq.begin() + i);
                layout.push_back(seq[0][0]);
                strength = 8;
                return;
            }
        }
        check_full_house();
        return;
    }

    void check_straight_flush() {
        for (auto i = col.begin(); i < col.end(); i++) {
            if((*i).size() >=5){
                layout.push_back((*i)[0]);
                for(auto j = (*i).begin() + 1; j < (*i).end(); j++){
                    if((*j).get_symbol() == ((*(j-1)).get_symbol() - 1)) {
                        layout.push_back(*j);
                        if(layout.size() == 5){
                            strength = 9;
                            return;
                        }
                    } else{
                        layout.clear();
                        layout.push_back(*j);
                    }
                }
                if(layout.size() == 4 and layout[0].get_symbol() == 3 and (*i)[0].get_symbol() == 12) {
                    layout.push_back((*i)[0]);
                    strength = 9;
                    return;
                }
                check_quads();
                return;
            }
        }
        check_quads();
        return;

    }

    void check() {
        std::sort(cards.rbegin(), cards.rend());
        set_seq();
        set_col();
        check_straight_flush();
        //print();
    }

    std::vector<Card> cards;
    int strength;
    std::vector<Card> layout;
    std::vector<std::vector<Card>> seq;
    std::vector<std::vector<Card>> col;
};


std::vector<Card> generate(int n) {
    std::vector<Card> cards;
    std::vector<int> v;
    for (int i = 0; i < 52; i++)
        v.push_back(i);
    for (int i = 0; i < n; i++) {
        int r = rand() % v.size();
        int s = v[r];
        int c = 0;
        while (s >= 13) {
            s -= 13;
            c += 1;
        }
        cards.push_back(Card(s, c));
        v.erase(v.begin() + r);
    }
    return cards;
}

int main() {
    srand(time(NULL));
    auto t = clock();
    for(int i = 0; i < 100000; i++) {
        std::vector<Card> cards = generate(7);
        Set s = Set(cards);
        //std::cout << std::endl << clock() - tt << std::endl;
    }
    /*
    int result[10];
    for(int i = 0; i < 10; i++){
        result[i] = 0;
    }
    Card aa = Card(sym(0),col(0));
    Card bb = Card(sym(0),col(0));
    Card cc = Card(sym(0),col(0));
    Card dd = Card(sym(0),col(0));
    Card ee = Card(sym(0),col(0));
    Card ff = Card(sym(0),col(0));
    Card gg = Card(sym(0),col(0));
    std::vector<Card> cards;
    cards.push_back(aa);
    cards.push_back(bb);
    cards.push_back(cc);
    cards.push_back(dd);
    cards.push_back(ee);
    cards.push_back(ff);
    cards.push_back(gg);
    for(int a = 0; a < 52; a++){
        for(int b = a+1; b < 52; b++){
            for(int c = b+1; c < 52; c++){
                for(int d = c+1; d < 52; d++){
                    std::cout << a << " " << b << " " << c  << " " << d <<  std::endl;
                    for(int e = d+1; e < 52; e++){
                        for(int f = e+1; f < 52; f++){
                            for(int g = f+1; g < 52; g++){
                                aa.set_color(col(a));
                                aa.set_symbol(sym(a));
                                bb.set_color(col(b));
                                bb.set_symbol(sym(b));
                                cc.set_color(col(c));
                                cc.set_symbol(sym(c));
                                dd.set_color(col(d));
                                dd.set_symbol(sym(d));
                                ee.set_color(col(e));
                                ee.set_symbol(sym(e));
                                ff.set_color(col(f));
                                ff.set_symbol(sym(f));
                                gg.set_color(col(g));
                                gg.set_symbol(sym(g));
                                Set s = Set(cards);
                                result[s.get_strength()-1]++;
                            }
                        }
                    }
                }
            }
        }
    }
    for(int i = 0; i < 10; i++){
        std::cout << result[i] << std::endl;
    }*/
    std::cout << std::endl << clock() - t << std::endl << std::endl;
    return 0;
}

