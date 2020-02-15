# Добавляет колонку с количеством ОКВЭДов и пересохраняет датасет

library(stringr)

all_ngo = read.csv('saratovsk_v1.csv',
                   encoding = 'UTF-8',
                   stringsAsFactors = F, 
                   na.strings = '')

all_ngo$okveds_num = str_count(all_ngo$allOkveds, "\n")

write.csv(all_ngo,
          'saratovsk_v1.csv', 
          row.names = F,
          fileEncoding = 'UTF-8',
          na = '')
