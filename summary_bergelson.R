library(jsonlite)
library(tidyverse)
library(stringr)

output_dir <- "/Volumes/psych/BergelsonLab/duplicate/"

#{r load_json}
# open json from file
json_file <- fromJSON("dup_result_pp.json", flatten=TRUE)

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
  mutate(top_folder = str_extract(duplicates, "/Volumes/psych/BergelsonLab/[^/]+/")) %>%
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

# filter again
# cleaned_dup <- cleaned_dup %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/VIP_data/image/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Stimuli/seedlings_stimuli/images_greybackground_960x960_150dpi/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Eyetracking ebd files/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/pho_checks/video/chi_cv_checks_round", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Stimuli/seedlings_stimuli/audio_stimuli_stereo_rightsilent_72db/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/old_aggregations/old_batch_basic_level/batch_basic_level_video_old/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/old_aggregations/batch_basic_level_video/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/old_aggregations/old_batch_basic_level/batch_basic_level_audio_old/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/old_aggregations/batch_basic_level_audio/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/LENA_Backup/lenamonth6_7_fiveminute/06_lena5min Folder/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Scripts_and_Apps/old_aggregations/lena5min_06_07/", duplicates))) %>%
#   filter(!(grepl("/Volumes/psych/BergelsonLab/Subject_Files/YM/", duplicates)))

# # print max number of ups for one file
# max(cleaned_dup$num_duplicates)
# ordered_table <- arrange(cleaned_dup, desc(num_duplicates))

write_csv(cleaned_dup, "cleaned_duplicates.csv")

