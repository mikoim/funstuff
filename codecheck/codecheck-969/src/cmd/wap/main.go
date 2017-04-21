package main

import (
	"github.com/lib/pq"
	"github.com/go-xorm/xorm"
	"github.com/gin-gonic/gin"
	"gopkg.in/go-playground/validator.v8"
	"strconv"
	"os"
	"time"
)

type Project struct {
	Id          int64     `xorm:"pk autoincr index" json:"id" validate:"min=0"`
	Url         string    `xorm:"varchar(255) null" json:"url"`
	Title       string    `xorm:"varchar(255) not null" json:"title" validate:"required"`
	Description string    `xorm:"text not null" json:"description" validate:"required"`
	Created     time.Time `xorm:"datetime not null" json:"-"`
}

type Sprint struct {
	Db        *xorm.Engine
	Validator *validator.Validate
}

func (s *Sprint) Run() error {
	var err error

	dsn, _ := pq.ParseURL(os.Getenv("DATABASE_URL"))
	db, err := xorm.NewEngine("postgres", dsn)
	if err != nil {
		return err
	}

	err = db.Sync(Project{})
	if err != nil {
		return err
	}

	s.Db = db

	s.Validator = validator.New(&validator.Config{TagName: "validate"})

	port := os.Getenv("PORT")

	r := gin.Default()

	r.GET("/api/projects", s.GetProjects)
	r.GET("/api/projects/:id", s.GetProjectsOne)
	r.POST("/api/projects", s.CreateProjects)
	r.DELETE("/api/projects/:id", s.DeleteProjects)

	r.Run(":" + port)

	return nil;
}

func (s *Sprint) GetProjectsOne(c *gin.Context) {
	var err error

	id, err := strconv.ParseInt(c.Params.ByName("id"), 10, 64)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "invalid id",
		})
		return
	}

	project := Project{}

	has, err := s.Db.Id(id).Get(&project)
	if err != nil || !has {
		c.JSON(404, gin.H{
			"error": "project not found",
		})
		return
	}

	c.JSON(200, project)
}

func (s *Sprint) GetProjects(c *gin.Context) {
	var projects []Project
	var err error

	offset, err := strconv.ParseInt(c.Request.URL.Query().Get("offset"), 10, 32)

	switch {
	case err == nil:
		err = s.Db.Limit(100, int(offset)).Find(&projects)
	default:
		err = s.Db.Limit(100).Find(&projects)
	}

	if err != nil {
		c.JSON(500, gin.H{
			"error": "something went wrong",
		})
		return
	}

	c.JSON(200, projects)
}

func (s *Sprint) CreateProjects(c *gin.Context) {
	url := c.PostForm("url")
	title := c.PostForm("title")
	description := c.PostForm("description")

	var project = Project{Url: url, Title: title, Description: description, Created: time.Now()}

	err := s.Validator.Struct(project)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "title and description must not be empty",
		})
		return
	}

	count, err := s.Db.Insert(&project)
	if err != nil || count == 0 {
		c.JSON(500, gin.H{
			"error": "something went wrong...",
		})
	} else {
		c.JSON(200, project)
	}
}

func (s *Sprint) DeleteProjects(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Params.ByName("id"), 10, 64)

	count, err := s.Db.Id(id).Delete(&Project{})

	switch {
	case count < 1:
		c.JSON(404, gin.H{
			"error": "project not found",
		})
	case err != nil:
		c.JSON(500, gin.H{
			"error": "something went wrong...",
		})
	default:
		c.JSON(200, gin.H{})
	}
}

func main() {
	s := Sprint{}
	if err := s.Run(); err != nil {
		panic(err)
	}
}
