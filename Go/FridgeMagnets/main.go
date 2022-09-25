package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

type WordGrouper struct {
	charsUsed map[byte]bool
}

const mod int = 1

var banned_words map[string]bool = map[string]bool{
	"adz":    true,
	"drys":   true,
	"blowzy": true,
	"nth":    true,
	"pyx":    true,
}

func readWords(wordlist_filename string) []string {
	dat, err := os.ReadFile(wordlist_filename)
	if err != nil {
		return []string{}
	}

	s := string(dat)
	words_raw := strings.Split(s, "\n")

	out := []string{"mr", "tv", "phd"}

	for _, word_raw := range words_raw {
		// if i%mod != 0 {
		// 	continue
		// }

		word := []rune{}
		valid := true
		used := map[rune]bool{}
		for _, c := range word_raw {
			if used[c] || c < 97 || c > 122 {
				valid = false
				break
			}
			word = append(word, c)
			used[c] = true
		}

		s := string(word)

		if valid && len(s) > 2 && !banned_words[s] {
			out = append(out, s)
		}
	}

	return out
}

var wordlist []string = readWords("/usr/share/dict/words")

var calls int = 0

func (w WordGrouper) dig(word_index int) []string {
	calls += 1

	word := wordlist[word_index]

	for i := range word {
		c := word[i]
		if w.charsUsed[c] {
			for j := i - 1; j >= 0; j -= 1 {
				delete(w.charsUsed, word[j])
			}
			return []string{}
		}
		w.charsUsed[c] = true
	}

	child := WordGrouper{
		charsUsed: w.charsUsed,
	}

	best := child.best(word_index)

	for i := range word {
		c := word[i]
		delete(w.charsUsed, c)
	}

	return best
}

const letters string = "abcdefghijklmnopqrstuvwxyz"

func (w WordGrouper) letters() string {
	out := ""
	for i := range letters {
		c := letters[i]
		if w.charsUsed[c] {
			out += string(c)
		}
	}
	return out
}

var seen_combos map[string]bool = map[string]bool{}

func (w WordGrouper) best(start int) []string {
	lets := w.letters()
	if seen_combos[lets] {
		return []string{}
	}
	seen_combos[lets] = true

	max_len := 0
	out := []string{}

	for word_index := start + 1; word_index < len(wordlist); word_index += 1 {
		s := w.dig(word_index)

		l := len(strings.Join(s, ""))

		if l > max_len {
			max_len = l
			out = s
		}
	}

	if start == -1 {
		return out
	}
	return append([]string{wordlist[start]}, out...)
}

func main() {
	start := time.Now().Unix()

	fmt.Println(mod)
	fmt.Println(len(wordlist))

	wg := WordGrouper{
		charsUsed: map[byte]bool{},
	}

	wl := wg.best(-1)

	fmt.Println(wl)
	fmt.Println(len(strings.Join(wl, "")))
	fmt.Println(float64(calls))
	fmt.Println(len(seen_combos))

	fmt.Println(time.Now().Unix() - start)
}
