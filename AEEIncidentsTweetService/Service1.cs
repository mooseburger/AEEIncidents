using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using System.Timers;
using HybridWindowsService;
using Npgsql;
using TweetSharp;


namespace AEEIncidentsTweetService
{
    public partial class Service1 : HybridServiceBase
    {
        Timer timer = new Timer();
        bool go = true;

        public Service1()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            //handle Elapsed event
            timer.Elapsed += new ElapsedEventHandler(OnElapsedTime);

            //One second interval
            timer.Interval = 60000;

            //enabling the timer
            timer.Enabled = true;
        }

        protected override void OnStop()
        {
        }

        private void OnElapsedTime(object source, ElapsedEventArgs e)
        {
            try
            {
                var service = new TwitterService("NCgdH3VLp5MGcCtvqBcEg", "ws9gH3IMMf7Me3yisICjRbog4Irove05PTMkBv1e8");
                service.AuthenticateWith("1486306525-RGwIIsWXfWlRiUTqQlSB6f1icA5ZTd806E3X1tz", "aZX45fWxpkdHa6ddHtEd4VHUamXzXEHkvVb174Mk");
                var incident = GetNextIncident();
                if (incident != null)
                {
                    service.SendTweet(new SendTweetOptions { Status = "Breakdown reported at " + incident.Item2 + " " + incident.Item4 + ", #" + incident.Item3.Replace(" ", "") + " - Status: " + incident.Item5 });
                }

                if (incident != null)
                {
                    IncidentPosted(incident.Item1);
                }
            }

            catch(Exception ex)
            {

            }
            //var status = service.SendTweet(new SendTweetOptions { Status = "Third Tweet!!!" });
        }

        private Tuple<string, string, string, string, string> GetNextIncident()
        {
            try
            {
                DataSet ds = new DataSet();
                DataTable dt = new DataTable();
                // PostgeSQL-style connection string
                string connstring = String.Format("Server={0};Port={1};" +
                    "User Id={2};Password={3};Database={4};",
                    "ec2-107-21-79-158.compute-1.amazonaws.com", "3600 ", "postgres",
                    "abca1234", "hack");
                NpgsqlConnection conn = new NpgsqlConnection(connstring);
                conn.Open();
                string sql = "SELECT * FROM public.events where posted = false order by created_at desc limit 1";
                // data adapter making request from our connection
                NpgsqlDataAdapter da = new NpgsqlDataAdapter(sql, conn);
                ds.Reset();
                // filling DataSet with result from NpgsqlDataAdapter
                da.Fill(ds);
                // since it C# DataSet can handle multiple tables, we will select first
                dt = ds.Tables[0];
                DataRow row = dt.Rows[0];
                Tuple<string, string, string, string, string> result = new Tuple<string, string, string, string, string>(row.ItemArray[0].ToString(), row.ItemArray[1].ToString(), row.ItemArray[3].ToString(), row.ItemArray[4].ToString(), row.ItemArray[5].ToString());
                // connect grid to DataTable
                // since we only showing the result we don't need connection anymore
                conn.Close();
                return result;
            }
            catch (Exception msg)
            {
                // something went wrong, and you wanna know why
                return null;
            }
        }
        private void IncidentPosted(string incidentId)
        {
            try
            {
                DataSet ds = new DataSet();
                DataTable dt = new DataTable();
                // PostgeSQL-style connection string
                string connstring = String.Format("Server={0};Port={1};" +
                   "User Id={2};Password={3};Database={4};",
                   "ec2-107-21-79-158.compute-1.amazonaws.com", "3600 ", "postgres",
                   "abca1234", "hack");
                NpgsqlConnection conn = new NpgsqlConnection(connstring);
                conn.Open();
                string sql = "Update public.events set posted = true where id = '" + incidentId + "'";
                // data adapter making request from our connection
                NpgsqlCommand da = new NpgsqlCommand(sql, conn);
                da.ExecuteNonQuery();
            }
            catch (Exception msg)
            {
            }
        }
    }
}
