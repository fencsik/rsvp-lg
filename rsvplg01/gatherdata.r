GatherData = function(dir=NULL, columns=NULL) {

    if (is.null(dir) || !dir.exists(dir)) return (NULL)

    fileList = list.files(path=dir, pattern="\\.csv$", full.names=TRUE,
                          recursive=TRUE, ignore.case=TRUE, no..=TRUE)
    allData = NULL
    for (fileName in fileList) {
        df = read.csv(fileName)
        if (is.null(columns)) {
            columns = names(df)
        }
        if (!all(columns %in% names(df))) {
            warning("missing columns in file ", fileName)
            next
        }
        if (is.null(allData)) {
            allData = df[columns]
        } else {
            allData = rbind(allData, df[columns])
        }
    }
    return(allData)
}
