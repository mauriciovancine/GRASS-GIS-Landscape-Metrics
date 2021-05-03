### script comparate landscape metrics grass gis###

# Mauricio Humberto Vancine - mauricio.vancine@gmail.com
# 25/07/2017

###---------------------------------------------------------------------------###

## memory
rm(list = ls())
gc()
memory.limit(size = 1.75e13) 

## packages
pacman::p_load(raster, rgdal, data.table, viridis, ggplot2, rasterVis, 
        GGally, dplyr, corrplot)

###---------------------------------------------------------------------------###

## import list of species
# directory
setwd("E:/github/GRASS-Landscape-Metrics/grassdb/RIO_CLARO")

# list files
la <- stack(dir(patt = ".tif"))
la

la.v <- data.table(rasterToPoints(la))[, -c(1, 2)]
la.v

dim(la.v)

###---------------------------------------------------------------------------###

## plot
# directory
dir.create("plots")
setwd("plots")

for(i in 1:length(names(la))){
 
 print(i)
 
 tiff(paste0("plot_", names(la[[i]]), ".tif"), wi = 18, he = 18, un = "cm", 
    res = 300, comp = "lzw+p")
 plot(la[[i]], col = viridis(100), main = names(la[[i]]))
 dev.off()
 
}

setwd("..")

###---------------------------------------------------------------------------###

## correlation

# directory
dir.create("correlation") 
setwd("correlation") 
getwd() 

# percentage
da.por <- sample_n(na.omit(la.v[, c(2, 5, 8)]), 10000)
colnames(da.por) <- c("PER patch", "PER core", "PER edge")
da.por

tiff("cor_por_plot.tif", wi = 18, he = 18, units = "cm", res = 300, comp = "lzw+p")
corrplot(cor(da.por),  type = "upper", diag = F, 
     tl.cex = .6, tl.srt = 20, addCoef.col = "black", number.cex = .8)
dev.off()

ggpairs(da.por, 
    lower = list(continuous = wrap(ggally_smooth, size = 1, color = "blue")),
    diag = list(continuous = wrap(ggally_barDiag, color = "blue")),
    upper = list(continuous = wrap(ggally_cor, color = "black"))) +
 theme(axis.text = element_text(size = 10, colour = "black"), 
    strip.text.x = element_text(size = 10),
    strip.text.y = element_text(size = 10), 
    panel.grid.major= element_line(colour = "white"))
ggsave("cor_por_des.tiff", wi = 18, he = 15, un = "cm", dpi = 300)


# diversity
da.div <- sample_n(na.omit(la.v[, c(1, 23:28)]), 10000)
colnames(da.div) <- c("DIV dominance", "DIV mpa", "DIV pielou", "DIV renyi_a05", 
           "DIV richness", "DIV shannon", "DIV simpson")
da.den

tiff("cor_div_plot.tif", wi = 18, he = 18, units = "cm", res = 300, comp = "lzw+p")
corrplot(cor(da.div),  type = "upper", diag = F, 
     tl.cex = .6, tl.srt = 20, addCoef.col = "black", number.cex = .7)
dev.off()

ggpairs(da.div, 
    lower = list(continuous = wrap(ggally_smooth, size = 1, color = "blue")),
    diag = list(continuous = wrap(ggally_barDiag, col = "blue")),
    upper = list(continuous = wrap(ggally_cor, col = "black"))) +
 theme(axis.text = element_text(size = 5, colour = "black"), 
    strip.text.x = element_text(size = 7),
    strip.text.y = element_text(size = 5), 
    panel.grid.major= element_line(colour = "white"))
ggsave("cor_div_des.tiff", wi = 18, he = 15, un = "cm", dpi = 300)


# r li
da.rli <- sample_n(na.omit(la.v[, c(14:22)]), 10000)
colnames(da.rli) <- c("rli edgedensity", "rli edgedensity_b", "rli mps",
           "rli padcv", "rli padrange", "rli padsd",
           "rli patchdensity", "rli patchnum", "rli shape")
da.rli

tiff("cor_rli_plot.tif", wi = 18, he = 18, units = "cm", res = 300, comp = "lzw+p")
corrplot(cor(da.rli),  type = "upper", diag = F, 
     tl.cex = .6, tl.srt = 20, addCoef.col = "black", number.cex = .7)
dev.off()

ggpairs(da.rli, 
    lower = list(continuous = wrap(ggally_smooth, size = 1, col = "blue")),
    diag = list(continuous = wrap(ggally_barDiag, color = "blue")),
    upper = list(continuous = wrap(ggally_cor, color = "black"))) + 
 theme(axis.text = element_text(size = 5, colour = "black"), 
    strip.text.x = element_text(size = 7),
    strip.text.y = element_text(size = 6),
    panel.grid.major= element_line(colour = "white"))
ggsave("cor_rli_des.tiff", wi = 18, he = 15, un = "cm", dpi = 300)


# connectivity
da.con <- sample_n(na.omit(la.v[, c(4, 13)]), 10000)
colnames(da.con) <- c("STR_CON patch", "FUN_CON patch")
da.con

tiff("cor_con_plot.tif", wi = 18, he = 18, units = "cm", res = 300, comp = "lzw+p")
corrplot(cor(da.con),  type = "upper", diag = T, 
     tl.cex = .6, tl.srt = 20, addCoef.col = "black", number.cex = .9)
dev.off()

ggpairs(da.con, 
    lower = list(continuous = wrap(ggally_smooth, size = 1, col = "blue")),
    diag = list(continuous = wrap(ggally_barDiag, color = "blue")),
    upper = list(continuous = wrap(ggally_cor, color = "black"))) + 
 theme(axis.text = element_text(size = 10, colour = "black"), 
    strip.text.x = element_text(size = 10),
    strip.text.y = element_text(size = 10),
    panel.grid.major= element_line(colour = "white"))
ggsave("cor_con_des.tiff", wi = 18, he = 15, un = "cm", dpi = 300)


# landscape
da.lan <- sample_n(na.omit(la.v[, c(2, 4:5, 8, 13:22)]), 10000)
colnames(da.lan) <- c("PER patch", "STR_CON patch", "PER core", "PER edge", 
           "FUN_CON patch", "rli edgedensity", "rli edgedensity_b", 
           "rli mps", "rli padcv", "rli padrange", "rli padsd",
           "rli patchdensity", "rli patchnum", "rli shape")
da.lan

tiff("cor_lan_plot.tif", wi = 18, he = 18, units = "cm", res = 300, comp = "lzw+p")
corrplot(cor(da.lan),  type = "upper", diag = F, 
     tl.cex = .6, tl.srt = 20, addCoef.col = "black", number.cex = .7)
dev.off()

ggpairs(da.lan, 
    lower = list(continuous = wrap(ggally_smooth, size = 1, col = "blue")),
    diag = list(continuous = wrap(ggally_barDiag, color = "blue")),
    upper = list(continuous = wrap(ggally_cor, size = 3, color = "black"))) + 
 theme(axis.text = element_text(size = 3, colour = "black"), 
    strip.text.x = element_text(size = 5),
    strip.text.y = element_text(size = 5),
    panel.grid.major= element_line(colour = "white"))
ggsave("cor_lan_des.tiff", wi = 18, he = 15, un = "cm", dpi = 300)

###---------------------------------------------------------------------------###

