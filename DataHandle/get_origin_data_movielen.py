from DataHandle.get_origin_data_base import Get_origin_data_base
import numpy as np
import pandas as pd
from config.model_parameter import model_parameter

np.random.seed(1234)


class Get_movie_data(Get_origin_data_base):

    def __init__(self, FLAGS):

        super(Get_movie_data, self).__init__(FLAGS = FLAGS)
        self.data_path = "data/orgin_data/movielen.csv"

        if FLAGS.init_origin_data == True:
            self.movie_data = pd.read_csv("data/raw_data/ml-20m/movies.csv")
            self.ratings_data = pd.read_csv("data/raw_data/ml-20m/ratings.csv")
            self.get_movie_data()
        else:
            self.origin_data = pd.read_csv(self.data_path)



    def get_movie_data(self):

        # user_filter = reviews_Electronics_df.groupby("user_id").count()
        # userfiltered = user_filter.sample(frac=0.22)
        # reviews_Electronics_df = reviews_Electronics_df[reviews_Electronics_df['user_id'].isin(userfiltered.index)]
        # print(reviews_Electronics_df.shape)
        self.logger.info(self.ratings_data.shape)
        user_filter = self.ratings_data.groupby("userId").count()
        userfiltered = user_filter.sample(frac=0.05)
        self.ratings_data = self.ratings_data[self.ratings_data['userId'].isin(userfiltered.index)]
        self.logger.info(self.ratings_data.shape)

        #进行拼接，进行格式的规范化
        self.origin_data = pd.merge(self.ratings_data,self.movie_data,on="movieId")
        self.origin_data = self.origin_data[["userId","movieId","timestamp","genres"]]
        self.origin_data = self.origin_data.rename(columns={"userId": "user_id",
                                         "movieId": "item_id",
                                         "timestamp":"time_stamp",
                                         "genres":"cat_id",
                                         })


        self.filtered_data = self.filter(self.origin_data)
        self.filtered_data.to_csv(self.data_path, encoding="UTF8", index=False)
        self.origin_data = self.filtered_data



if __name__ == "__main__":
    model_parameter_ins = model_parameter()
    experiment_name = model_parameter_ins.flags.FLAGS.experiment_name
    FLAGS = model_parameter_ins.get_parameter(experiment_name).FLAGS

    ins = Get_movie_data(FLAGS=FLAGS)
    ins.getDataStatistics()










