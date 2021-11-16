package main
import (
	"database/sql"
)

// Tea Model
type Tea struct {
	ID          int
	Name        string
	Location    string
	Description string
	Country     string
}

func getCountry(locationName string) (countryName string, err error) {
	var locationID int
	row := db.QueryRow("SELECT id FROM locations WHERE name = ?", locationName)
	err = row.Scan(&locationID)
	if err != nil {
		return countryName, err
	}
	var countryID int
	row = db.QueryRow("SELECT location_to_id FROM location_relations WHERE location_from_id = ?", locationID)
	err = row.Scan(&countryID)
	if err != nil {
		return countryName, err
	}
	row = db.QueryRow("SELECT name FROM locations WHERE id = ?", countryID)
	err = row.Scan(&countryName)
	if err != nil {
		return countryName, err
	}
	return countryName, err
}

func getAllTeas() (teas []Tea, err error) {
	rows, err := db.Query("SELECT * FROM teas ORDER BY id DESC")
	defer rows.Close()
	if err != nil {
		return teas, err
	}
	for rows.Next() {
		tea := Tea{}
		err = rows.Scan(&tea.ID, &tea.Name, &tea.Location, &tea.Description)
		if err != nil {
			return teas, err
		}
		teas = append(teas, tea)
	}
	return teas, err
}

func postNewTea(name string, locationName string, description string) (err error) {
	var location_exist int
	row := db.QueryRow("SELECT 1 FROM locations WHERE name = ?", locationName)
	err = row.Scan(&location_exist)

	if err != nil && err != sql.ErrNoRows {
		return err
	}
	if location_exist == 1 {
		db.Exec("INSERT INTO teas (name, location, description) VALUES (?, ?, ?)", name, locationName, description)
	}
	return nil
}
