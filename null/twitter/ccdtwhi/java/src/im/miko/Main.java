package im.miko;

import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        System.out.printf("ccdtws (0.1.0.1)\n");

        while (true) {
            try {
                Class.forName("com.mysql.jdbc.Driver").newInstance();

                ConfigurationBuilder cb = new ConfigurationBuilder();
                cb.setDebugEnabled(true)
                        .setOAuthConsumerKey("")
                        .setOAuthConsumerSecret("")
                        .setOAuthAccessToken("")
                        .setOAuthAccessTokenSecret("");
                TwitterFactory tf = new TwitterFactory(cb.build());
                Twitter twitter = tf.getInstance();

                List<User> userList = new ArrayList<User>();
                Long cursor = -1L;

                do {
                    PagableResponseList<User> response = null;
                    response = twitter.getUserListMembers("bolezn", "ccd", cursor);

                    for (User user : response) {
                        userList.add(user);
                    }

                    cursor = response.getNextCursor();
                } while (cursor > 0);

                Connection c = DriverManager.getConnection("jdbc:mysql://localhost/ccd?user=ccd&password=&characterEncoding=utf8");
                PreparedStatement p = c.prepareStatement("INSERT INTO `ccd`.`tws` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);");

                long time = System.currentTimeMillis() / 1000;

                for (User u : userList) {
                    p.clearParameters();

                    p.setLong(1, u.getId());
                    p.setString(2, u.getScreenName());
                    p.setString(3, u.getName());
                    p.setInt(4, u.getStatusesCount());
                    p.setInt(5, u.getFavouritesCount());
                    p.setInt(6, u.getFriendsCount());
                    p.setInt(7, u.getFollowersCount());
                    p.setString(8, u.getOriginalProfileImageURL());
                    p.setLong(9, u.getCreatedAt().getTime() / 1000);
                    p.setLong(10, time);

                    p.execute();
                }
            } catch (InstantiationException e) {
                e.printStackTrace();
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
            } catch (SQLException e) {
                e.printStackTrace();
            } catch (TwitterException e) {
                e.printStackTrace();
            }

            System.out.printf("The DB was updated!\n");

            try {
                System.out.printf("Sleeping...\n");
                Thread.sleep(1800000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
