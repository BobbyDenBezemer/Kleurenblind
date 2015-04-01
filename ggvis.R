### GGvis tutorial

# SImple scatterplot
mtcars %>% ggvis(~wt, ~mpg, fill := "red") %>% layer_points()

# Scatterplot with regression line
mtcars %>% 
  ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  layer_model_predictions(model = "lm", se = TRUE)

# Scatterplot with fill
mtcars %>% 
  ggvis(~wt, ~mpg) %>% 
  layer_points(fill = ~factor(cyl))

# Coloring points and applying a smoother to each level of factor
mtcars %>% 
  ggvis(~wt, ~mpg, fill = ~factor(cyl)) %>% 
  layer_points() %>% 
  group_by(cyl) %>% 
  layer_model_predictions(model = "lm")

## Bar graphs
pressure %>% 
  ggvis(~temperature, ~pressure) %>%
  layer_bars()

## Line graphs
pressure %>% 
  ggvis(~temperature, ~pressure) %>% 
  layer_lines()

pressure %>% 
  ggvis(~temperature, ~pressure) %>%
  layer_points() %>% 
  layer_lines()

## Histograms
faithful %>% 
  ggvis(~eruptions) %>% 
  layer_histograms(width=0.5, boundary = 0)

cocaine %>% ggvis(~month, fill := "red") %>%
  layer_histograms() %>%
  add_axis("x", title = "month") %>%
  add_axis("y", title = "count")

## Adding text layers
df %>% 
  ggvis(~x, ~y, text := ~label) %>% 
  layer_text(fontSize := 50)

## make interactivity
mtcars %>%
  ggvis(~wt, ~mpg) %>%
  layer_smooths(span = input_slider(0.5, 1, value = 1)) %>%
  layer_points(size := input_slider(100, 1000, value = 100))

# 
mtcars %>% ggvis(~mpg, input_select(names(mtcars), map = as.name)) %>% layer_lines()
diamonds %>%
  ggvis(~x, ~price, fill = input_radiobuttons(names(diamonds), map = as.name)) %>%
  layer_points()

# Plot that has both slider and select box
mtcars %>% ggvis(x = ~wt) %>%
  layer_densities(
    adjust = input_slider(.1, 2, value = 1, step = .1, label = "Bandwidth adjustment"),
    kernel = input_select(
      c("Gaussian" = "gaussian",
        "Epanechnikov" = "epanechnikov",
        "Rectangular" = "rectangular",
        "Triangular" = "triangular",
        "Biweight" = "biweight",
        "Cosine" = "cosine",
        "Optcosine" = "optcosine"),
      label = "Kernel")
    )

mtcars %>%
  ggvis(~wt, ~mpg, size := input_slider(10, 1000)) %>%
  layer_points(fill := "red") %>%
  layer_points(stroke := "black", fill := NA)

mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points(size := input_slider(100, 1000, label = "black")) %>%
  layer_points(fill := "red", size := input_slider(100, 1000, label = "red"))

## Creating custom styles

# Customizing Axes
mtcars %>% ggvis(~wt, ~mpg) %>% layer_points() %>%
  add_axis("x", title = "Weight") %>%
  add_axis("y", title = "Miles per gallon")

# Use title offset to push the titles further away
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x", title = "Weight", title_offset = 50) %>%
  add_axis("y", title = "Miles per gallon", title_offset = 50)

# Ticks and padding
# Change ticks and subdivide with minor ticks
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x", subdivide = 9, values = 1:6) %>%
  add_axis("y", subdivide = 1, values = seq(10, 34, by = 2))

# Make the minor ticks smaller and the end ticks longer
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x", subdivide = 9, values = 1:6, tick_size_major = 10,
           tick_size_minor = 5, tick_size_end = 15, tick_padding = 20)

# Orientation
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x", orient = "top") %>%
  add_axis("y", orient = "right")

# Axes on both sides
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x", orient = "bottom") %>%
  add_axis("x", orient = "top")

# put multiple sides
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x") %>%
  add_axis("x", offset = 40, grid = FALSE)

## Legends
mtcars2 %>% ggvis(~mpg, ~wt, size = ~cyl, fill = ~cyl) %>% layer_points() %>%
  add_legend(c("size", "fill"))

# More customized axes
mtcars %>% ggvis(~wt, ~mpg) %>%
  layer_points() %>%
  add_axis("x", properties = axis_props(
    axis = list(stroke = "red", strokeWidth = 5),
    grid = list(stroke = "blue"),
    ticks = list(stroke = "blue", strokeWidth = 2),
    labels = list(angle = 45, align = "left", fontSize = 20)
  ))

