### Collect each subject's data file into a tab-delimited text file

f.rawdata <- function () {
    datadir <- "data"
    txtfile <- "AllData.txt"
    rdafile <- "AllData.rda"
    thisfile <- "rawdata.r"

    infiles <- file.path(datadir, dir(datadir))

    varnames <- NULL
    varnamesFromFile <- NULL
    rawdata <- NULL

    for (f in infiles) {
        if (!file.exists(f)) stop("cannot find input file ", f)
        cat("Opening data file ", f, "...", sep = "")
        dt <- read.csv(f)

        if (is.null(varnames)) {
            varnames <- colnames(dt)
            varnamesFromFile <- f
        } else if (dim(dt)[2] != length(varnames) || !all(names(dt) == varnames)) {
            warning("column names in ", f, " do not match those in ", varnamesFromFile)
            dt <- dt[, varnames]
        }

        if (is.null(rawdata)) {
            rawdata <- dt
        } else {
            rawdata <- rbind(rawdata, dt)
        }
        cat("done\n")
    }

    write.table(rawdata, file=txtfile, sep="\t", quote=F, row.names=F);
    save(rawdata, file=rdafile)
}

f.rawdata()
rm(f.rawdata)
