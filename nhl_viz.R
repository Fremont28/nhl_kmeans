def_group=read.csv("coconut_juice.csv")
def_group$Group<-as.factor(def_group$Group)
def_group1=subset(def_group,sellect=c(2,3,4,13,17,21,25,34,36,37,38,39,40,42,44))

#libraries
library(plyr)
library(dplyr)
library(stringr)
library(lettercase)
library(plotly)
library(ggplot2)

#mean by group
summary(def_group$Group) 
group_avg=def_group %>% 
  group_by(Group) %>%
  summarise_all("mean")
group_avg1=subset(group_avg,select=c("Group","P.60","CF.","xGF","ZSR","ice_time.game","iP...","TOI..QoT","TOI.","PDO"))

#group three ice-loggers 
g3=subset(def_group,Group=="3",select=c("Player"))
g3 
g2=subset(def_group,Group=="2",select=c("Player"))
g2
g0=subset(def_group,Group=="0",select=c("Player"))
g0
g4=subset(def_group,Group=="4",select=c("Player"))
g4
g1=subset(def_group,Group=="1",select=c("Player"))
g1
cor.test(group_avg$CF.,group_avg$xGF.) #0.90 correlation 

#point shares and groupings
ps=read.csv("ps.csv")
ps$Player<-as.character(ps$Player)
ps1=str_all_caps(ps$Player)

x=str_replace_all(def_group$Player,"[[:punct:]]","")
x1=gsub(" ", "", x) 
x2=as.data.frame(x1)
colnames(x2)[1]<-"Player"

ps2=gsub(" ","",ps1)
ps3=as.data.frame(ps2)
ps4=cbind(ps3,ps$PS,ps$OPS,ps$DPS)
colnames(ps4)[1] <- "Player"
colnames(ps4)[2] <- "PS"
colnames(ps4)[3] <- "OPS"
colnames(ps4)[4] <- "DPS"

finals=merge(ps4,x2,by="Player")

r=str_replace_all(def_group$Player,"[[:punct:]]","")
r1=as.data.frame(r)
colnames(r1)[1]="Player"
colnames(def_group)[2]="player_x"
r2=cbind(def_group,r1)

finals1=merge(finals,r2,by="Player") 
group_ps=subset(finals1,Group=="0")
group_avg2=finals1 %>% 
  group_by(Group) %>%
  summarise_all("mean")
group_avg_finals=subset(group_avg2,select=c("Group","P.60","CF.","xGF","ZSR","ice_time.game","iP...","TOI..QoT","TOI.","PDO","PS","OPS","DPS"))

#summary statistics
names(def_group) 
mean(def_group$iCF.60)
max(def_group$iCF.60)
cor.test(def_group$ZSR,def_group$CF.)
count(def_group$Group)
#group 3
g3_metrics<-subset(def_group,def_group$Rel.xGF.<0 & def_group$Group=="3")
g3_metrics["player_x"]
cor.test(def_group$ixGF.60,def_group$Rel.xGF.)

#1. density plot 
names(def_group)
p=ggplot(def_group,aes(x=iSh.,fill=Group))+
  geom_density(alpha=0.5,position="stack")

#horz. bar plot
p1=plot_ly(group_avg_finals,x=~PS,y=~Group,type='bar',
           orientation='h',name='Group',
           marker=list(color='rgba(246, 78, 139, 0.6)',
                       line = list(color = 'rgba(246, 78, 139, 1.0)',
                                   width = 3)) %>%
             layout(title="ice",xaxis=list(type="category",title="donut")))

#overlay histogram 
p2=ggplot(def_group,aes(x=iCF.60))+
  geom_histogram(aes(y=..density..),alpha=0.7,
                 fill="#333333")+geom_density(fill="#ff4d4d", alpha = 0.5)+
  theme(panel.background = element_rect(fill = '#ffffff'))+xlab("Corsi For per 60 minutes")


subx=subset(def_group,def_group$Rel.xGF.> -6)
p3=ggplot(subx,aes(x=subx$Rel.xGF.,y=subx$ixGF.60,color=subx$Group))+
  geom_point(shape=1)+geom_text(aes(label=ifelse(subx$Group=="3" & 
                                                   subx$Rel.xGF.<0,
                                                 as.character(subx$player_x),'')),
                                hjust=0,vjust=0)+xlab("Relative Expected Goals")+
  ylab("Expected Goals For/60 Minutes")

p4=ggplotly(p3)

#scatterplot
p3=ggplot(subx,aes(x=subx$Rel.xGF.,y=subx$ixGF.60,color=subx$Group))+
  geom_point(shape=1)+labs(x="Relative Expected Goals",y="Expected Goals For/60 Minutes",
                           color="Group")+
  geom_text(aes(label=ifelse(subx$Group=="3" & 
                               subx$Rel.xGF.<0,
                             as.character(subx$player_x),'')),
            hjust=0,vjust=0)

