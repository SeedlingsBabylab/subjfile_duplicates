library(jsonlite)
library(tidyverse)
library(stringr)

output_dir <- "/Volumes/pn-opus/Seedlings/duplicate/"

#{r load_json}
# open json from file
json_file <- fromJSON("dup_result_other.json", flatten=TRUE)

# display columns of json file
colnames(json_file)

# switch to df
dup_df <- as.data.frame(json_file)


#{r filtering}
# remove Pages.app, SSI/ssi[...], .DS_Store
cleaned_dup <- dup_df %>% 
  filter(!(grepl("Pages", duplicates))) %>%
  filter(!(grepl("/SSI/ssi-master/", duplicates))) %>%
  filter(!(grepl("model.id2word", duplicates))) %>%
  filter(!(grepl("/.git/", duplicates))) %>%
  filter(!(grepl(".DS_Store", duplicates)))

# add column with index of duplicate
cleaned_dup$ID <- seq.int(nrow(cleaned_dup))

# separate duplicates on several rows
cleaned_dup <- cleaned_dup %>%
  unnest(duplicates)
# add column with file type and top folder
cleaned_dup <- cleaned_dup %>%
  mutate(type = str_extract(duplicates, "\\.[^/]+$"))

# get all file type
all_folder <- cleaned_dup %>%
  group_by(num_duplicates, type) %>%
  summarise(count = n()) %>%
  spread(num_duplicates, count) %>%
  replace(., is.na(.), 0) %>%
  mutate(total_count = rowSums(select(., -type)))

write_csv(all_folder, paste(output_dir, "total_duplicate_count.csv", sep = ""))


# summary table for each top folder
each_folder <- cleaned_dup %>%
  mutate(top_folder = str_extract(duplicates, "/Volumes/pn-opus/Seedlings/[^/]+/")) %>%
  split(.$top_folder)

for (k in 1:length(each_folder)) {
  each_folder[[k]] <- each_folder[[k]] %>%
    select(-c(top_folder)) %>%
    group_by(num_duplicates, type) %>%
    summarise(count = n()) %>%
    spread(num_duplicates, count) %>%
    replace(., is.na(.), 0) %>%
    mutate(total_count = rowSums(select(., -type)))
  
  file_name <- paste(output_dir, str_replace_all(str_extract(names(each_folder)[k], "/[^/]+/$"), "/", ""), "_duplicate_count.csv", sep = "")
  write_csv(each_folder[[k]], file_name)
}

write_csv(cleaned_dup, "cleaned_duplicates.csv")

