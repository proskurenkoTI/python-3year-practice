package main

import (
	"fmt"
	"log/slog"
	"net/http"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/xuri/excelize/v2"
)

type Vessel struct {
	Name       string
	IMO        string
	MMSI       string
	TypeVessel string
}

func getShipData(url string) (Vessel, error) {
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		slog.Error("Error creating request: ", err)
	}

	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
	req.Header.Set("Accept-Language", "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7")
	req.Header.Set("Referer", "https://www.vesselfinder.com/")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return Vessel{}, fmt.Errorf("Error sending request: %s", err)
	}
	slog.Info("Response Status: ", resp.Status)
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return Vessel{}, fmt.Errorf("Error parsing response: %s", err)
	}

	shipLink := ""
	cnt := 0
	doc.Find(".ship-link").Each(func(i int, s *goquery.Selection) {
		shipLink, _ = s.Attr("href")
		cnt++
	})
	if cnt != 1 {
		return Vessel{}, fmt.Errorf("No ship link found")
	}

	req, err = http.NewRequest("GET", "https://www.vesselfinder.com"+shipLink, nil)

	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		slog.Error("Error sending request: ", err)
	}
	defer resp.Body.Close()

	doc, err = goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return Vessel{}, fmt.Errorf("Error parsing response: %s", err)
	}

	var imo, mmsi, name, typeVessel string
	doc.Find(".title").Each(func(i int, s *goquery.Selection) {
		name = s.Text()
	})

	doc.Find(".aparams, .tpt1").Each(func(i int, table *goquery.Selection) {
		table.Find("tr").Each(func(i int, row *goquery.Selection) {
			value := strings.TrimSpace(row.Find("td").Text())

			if strings.Contains(strings.ToUpper(value), "IMO") {
				imo, _ = strings.CutPrefix(value, "IMO номер")

			}
			if strings.Contains(strings.ToUpper(value), "MMSI") && !strings.Contains(strings.ToUpper(value), "IMO / MMSI") {
				mmsi, _ = strings.CutPrefix(value, "MMSI")
			}

			if strings.Contains(strings.ToUpper(value), "IMO / MMSI") || strings.Contains(strings.ToUpper(value), "ENI / MMSI") {
				lastSpace := strings.LastIndex(value, " ")
				mmsi = value[lastSpace+1:]
			}

			if strings.Contains(value, "Тип") && !strings.Contains(value, "топлива") && !strings.Contains(value, "двигателя") {
				typeVessel, _ = strings.CutPrefix(value, "Тип")
			} else if strings.Contains(value, "AIS тип") {
				typeVessel, _ = strings.CutPrefix(value, "AIS тип")
			}

			if imo != "" && mmsi != "" && typeVessel != "" {
				return
			}
		})
	})

	return Vessel{
		Name:       strings.TrimSpace(name),
		IMO:        strings.TrimSpace(imo),
		MMSI:       strings.TrimSpace(mmsi),
		TypeVessel: strings.TrimSpace(typeVessel),
	}, nil
}

func readFile(path string) []string {
	f, err := excelize.OpenFile(path)
	if err != nil {
		slog.Error("fail open file: ", err)
		return nil
	}
	defer func() {
		if err := f.Close(); err != nil {
			slog.Error("Ошибка закрытия файла: %v", err)
		}
	}()

	var links []string

	sheetName := f.GetSheetName(0)
	if sheetName == "" {
		slog.Error("fail get sheet name")
		return nil
	}

	rows, err := f.GetRows(sheetName)
	if err != nil {
		slog.Error("fail get rows: ", err)
		return nil
	}

	for _, row := range rows {
		if len(row) > 0 {
			link := row[0]
			if link != "" {
				link = strings.ReplaceAll(link, " ", "%20")
				links = append(links, link)
			}
		}
	}

	links = links[1:]
	return links
}

func writeFile(vessels []Vessel, filename string) error {
	f := excelize.NewFile()

	sheetName := "Vessels"
	index, err := f.NewSheet(sheetName)
	if err != nil {
		return fmt.Errorf("failed create sheet: %v", err)
	}

	headers := []string{"Название", "IMO", "MMSI", "Тип"}
	for i, header := range headers {
		cell, _ := excelize.CoordinatesToCellName(i+1, 1)
		f.SetCellValue(sheetName, cell, header)
	}

	for i, vessel := range vessels {
		row := i + 2

		cell1, _ := excelize.CoordinatesToCellName(1, row)
		f.SetCellValue(sheetName, cell1, vessel.Name)

		cell2, _ := excelize.CoordinatesToCellName(2, row)
		f.SetCellValue(sheetName, cell2, vessel.IMO)

		cell3, _ := excelize.CoordinatesToCellName(3, row)
		f.SetCellValue(sheetName, cell3, vessel.MMSI)

		cell4, _ := excelize.CoordinatesToCellName(4, row)
		f.SetCellValue(sheetName, cell4, vessel.TypeVessel)
	}

	f.SetActiveSheet(index)

	if err := f.SaveAs(filename); err != nil {
		return fmt.Errorf("failed save file: %v", err)
	}

	if err := f.Close(); err != nil {
		return fmt.Errorf("failed close file: %v", err)
	}

	slog.Info("file save success!: ", filename)
	return nil
}

func main() {
	links := readFile("Links.xlsx")
	fmt.Printf("Found %d links\n", len(links))
	var vessels []Vessel

	for i, link := range links {
		fmt.Println(i, "process:", link)
		vesel, err := getShipData(link)
		if err != nil {
			slog.Error("fail get ship data: ", err)
			continue
		}
		vessels = append(vessels, vesel)
	}

	err := writeFile(vessels, "result.xlsx")
	if err != nil {
		slog.Error("Failed write to file", err)
	} else {
		fmt.Println("A write success!")
	}
}
