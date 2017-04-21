package main

import (
	"fmt"
	"math/rand"
	"time"
	"container/list"
)

func doit(maxPerson int) (int, []int) {
	maxTime := 600
	limitJoinTime := 300

	sliceJoin := make([]int, limitJoinTime)
	historySlice := make([]int, maxTime)

	listPerson := list.New()

	// お客様を追加
	for i := 0; i < maxPerson; i++ {
		sliceJoin[rand.Intn(limitJoinTime - 1)]++
	}

	waitTime := 0
	waitTime2 := 0

	for i := 0; i < maxTime; i++ {
		// 待ち行列にお客様を追加
		if i < 300 && sliceJoin[i] > 0 {
			for j := 0; j < sliceJoin[i]; j++ {
				listPerson.PushBack(rand.Intn(10) + 15)
			}
		}

		// お客様に対応する エリート
		if waitTime == 0 && listPerson.Len() > 0 {
			person := listPerson.Front()
			waitTime = rand.Intn(10) + 15
			listPerson.Remove(person)
		} else if (waitTime > 0) {
			waitTime--

			if waitTime == 0 && listPerson.Len() > 0 {
				person := listPerson.Front()
				waitTime = person.Value.(int)
				listPerson.Remove(person)
			}
		}

		// お客様に対応する NOOB
		if waitTime2 == 0 && listPerson.Len() > 0 {
			person := listPerson.Front()
			waitTime2 = rand.Intn(30) + 20
			listPerson.Remove(person)
		} else if (waitTime2 > 0) {
			waitTime2--

			if waitTime2 == 0 && listPerson.Len() > 0 {
				person := listPerson.Front()
				waitTime2 = person.Value.(int)
				listPerson.Remove(person)
			}
		}

		// 履歴に列の長さを追加
		historySlice[i] = listPerson.Len()

	}

	maxValue := historySlice[0]

	for _, value := range historySlice {
		if value > maxValue {
			maxValue = value
		}
	}

	return maxValue, historySlice
}

func sliceAdd(a []int, b []int) ([]int) {
	result := make([]int, 600)

	for i := 0; i < 600; i++ {
		result[i] = a[i] + b[i];
	}

	return result;
}

func sliceDiv(a []int, b float64) ([]float64) {
	result := make([]float64, 600)

	for i := 0; i < 600; i++ {
		result[i] = float64(a[i]) / b;
	}

	return result;
}

func main() {
	rand.Seed(time.Now().Unix())

	for lol := 0; lol <= 50; lol += 5 {
		total := 0.0

		result := make([]int, 600)

		for i := 0; i < 10000; i++ {
			var queueLength int
			var historySlice []int

			queueLength, historySlice = doit(lol)
			total += float64(queueLength)

			result = sliceAdd(result, historySlice)
		}

		fmt.Println("######", lol, total/10000)

		for i := 0; i < 600; i++ {
			fmt.Println(i + 1, float64(result[i]) / 10000)
		}
	}
}
