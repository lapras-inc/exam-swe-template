package main

import (
	"database/sql"
	"math"
	"net/http"
	"strconv"
	"unicode/utf8"

	"github.com/flosch/pongo2"
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB
var TEAS_PER_PAGE = 6

func main() {
	// database setting
	user := "scouty"
	pass := "scouty"
	dbname := "scoutea"
	db, _ = sql.Open("mysql", user+":"+pass+"@/"+dbname)
	db.SetMaxIdleConns(5)

	gin.SetMode(gin.DebugMode)
	r := gin.Default()
	r.Use(static.Serve("/css", static.LocalFile("css", true)))

	// GET /
	r.GET("/", func(c *gin.Context) {
		page, err := strconv.Atoi(c.Query("page"))
		if err != nil {
			page = 1
		}
		query := c.Query("query")
		offset := (page - 1) * TEAS_PER_PAGE

		teas, err := getAllTeas()
		if err != nil {
			panic(err.Error())
		}
		teasMatch := []Tea{}
		for _, tea := range teas {
			if query == "" {
				teasMatch = append(teasMatch, tea)
				continue
			}
			tea.Country, err = getCountry(tea.Location)
			if err != nil {
				panic(err.Error())
			}
			if query == tea.Name || query == tea.Location || query == tea.Country {
				teasMatch = append(teasMatch, tea)
			}
		}

		teasDisplay := []Tea{}
		for i, tea := range teasMatch {
			if offset <= i && i < offset+TEAS_PER_PAGE {
				tea.Country, err = getCountry(tea.Location)
				if err != nil {
					panic(err.Error())
				}
				if utf8.RuneCountInString(tea.Description) > 100 {
					tea.Description = string([]rune(tea.Description)[:100]) + "..."
				}
				teasDisplay = append(teasDisplay, tea)
			}
		}

		firstPage := 1
		currentPage := page
		lastPage := int(math.Ceil(float64(len(teasMatch)) / float64(6)))
		urlQuery := ""
		if query != "" {
			urlQuery = "&query=" + query
		}

		tpl, err := pongo2.FromFile("templates/index.html")
		if err != nil {
			c.String(500, "Internal Server Error")
		}
		err = tpl.ExecuteWriter(pongo2.Context{
			"teas":        teasDisplay,
			"query":       query,
			"urlQuery":    urlQuery,
			"firstPage":   firstPage,
			"currentPage": currentPage,
			"lastPage":    lastPage,
		}, c.Writer)
		if err != nil {
			c.String(500, "Internal Server Error")
		}
	})

	r.GET("/new", func(c *gin.Context) {
		tpl, err := pongo2.FromFile("templates/new.html")
		if err != nil {
			c.String(500, "Internal Server Error")
		}
		err = tpl.ExecuteWriter(pongo2.Context{}, c.Writer)
		if err != nil {
			c.String(500, "Internal Server Error")
		}
	})

	r.GET("/initialize", func(c *gin.Context) {
		db.Exec("DELETE FROM teas WHERE id > 500000")
		db.Exec("DELETE FROM locations WHERE id > 2397")
		db.Exec("DELETE FROM location_relations WHERE id > 2394")

		c.Redirect(http.StatusFound, "/")
	})

	r.POST("/", func(c *gin.Context) {
		name := c.PostForm("name")
		location := c.PostForm("location")
		description := c.PostForm("description")
		postNewTea(name, location, description)

		c.Redirect(http.StatusFound, "/")
	})

	r.Static("/css", "css")
	r.Run(":8080")
}
