namespace Loupedeck.DemoPlugin
{
    using System;
    using System.Timers;


    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Net;
    using System.Text;
    using System.Threading.Tasks;
    using System.Web;

    class ButtonSwitchesCommand : PluginDynamicCommand
    {
        private readonly Boolean[] _switches = new Boolean[12];
        private Timer _newTimer = new Timer();

        private readonly String _image0ResourcePath;
        private readonly String _image1ResourcePath;


        public ButtonSwitchesCommand() : base()
        {
            this._newTimer.Elapsed += new ElapsedEventHandler(this.DisplayTimeEvent);
            this._newTimer.Interval = 5000;
            this._newTimer.Start();

            this._image0ResourcePath = EmbeddedResources.FindFile("ToggleSwitchButton0.png");
            this._image1ResourcePath = EmbeddedResources.FindFile("ToggleSwitchButton1.png");

            for (var i = 0; i < 12; i++)
            {
                // parameter is the switch index
                var actionParameter = i.ToString();

                // add parameter
                this.AddParameter(actionParameter, $"Switch {i}", "Switches");
            }
        }

        protected override void RunCommand(String actionParameter)
        {

            var url0 = $"https://junction2021.herokuapp.com/highlight";

            var pending = GetApi(url0).Replace('"', '[').Replace("[", "").Replace("]", "").Trim().Split(',');

            if (Int32.TryParse(actionParameter, out var i))
            {
                var url = $"https://junction2021.herokuapp.com/top_users/{i}";
                var user = GetApi(url);


                if (user != "0")
                {
                    user = user.Replace('"', '[').Replace("[", "").Replace("]", "").Trim();
                    user = user.Split(',')[0];
                    if (pending.Contains(user))
                    {
                        var url1 = $"https://junction2021.herokuapp.com/highlight/{user}";
                        GetApi(url1);
                    }

                }
            }
            this.ActionImageChanged(actionParameter);

        }

            protected void DisplayTimeEvent(object source, ElapsedEventArgs e)
        {
            this.RunCommand("0");
        }
        /*
        protected override String GetCommandDisplayName(String actionParameter, PluginImageSize imageSize)
        {

            if (Int32.TryParse(actionParameter, out var i))
            {
                return "huutis";
            }

            else
            {
                return null;
            }

        }
        */
        /*
        protected override String GetCommandDisplayName(String actionParameter, PluginImageSize imageSize)
        {

            if (Int32.TryParse(actionParameter, out var i))
            {

                var url = $"https://junction2021.herokuapp.com/top_users/{i}";
                var user = GetApi(url);

                //var exists = users.ElementAtOrDefault(i) != null;
                if (user != "0")
                {
                    user = user.Replace('"', '[').Replace("[", "").Replace("]", "");
                    return user.Split(',')[0];

                }
                else
                {
                    return $"Switch {i}: {this._switches[i]}";
                }
            }
            else
            {
                return null;
            }
        }
        */
        protected override BitmapImage GetCommandImage(String actionParameter, PluginImageSize imageSize)
        {
            var url0 = $"https://junction2021.herokuapp.com/highlight";

            var pending = GetApi(url0).Replace('"', '[').Replace("[", "").Replace("]", "").Trim().Split(',');

            if (Int32.TryParse(actionParameter, out var i))
            {
                var url = $"https://junction2021.herokuapp.com/top_users/{i}";
                var user = GetApi(url);


                if (user != "0")
                {
                    user = user.Replace('"', '[').Replace("[", "").Replace("]", "").Trim();
                    user = user.Split(',')[0];
                    if (pending.Contains(user))
                    {
                        using (var bitmapBuilder = new BitmapBuilder(imageSize))
                        {
                            bitmapBuilder.SetBackgroundImage(EmbeddedResources.ReadImage(this._image1ResourcePath));
                            bitmapBuilder.DrawText(user);

                            return bitmapBuilder.ToImage();
                        }
                    }
                    else
                    {
                        using (var bitmapBuilder = new BitmapBuilder(imageSize))
                        {
                            bitmapBuilder.SetBackgroundImage(EmbeddedResources.ReadImage(this._image0ResourcePath));
                            bitmapBuilder.DrawText(user);

                            return bitmapBuilder.ToImage();
                        }

                    }


                }
                else
                {
                    return EmbeddedResources.ReadImage(this._image0ResourcePath);
                }

            }
            else
            {
                return EmbeddedResources.ReadImage(this._image0ResourcePath);
            }
        }

        private static String GetApi(String ApiUrl)
        {

            var responseString = "";
            var request = (HttpWebRequest)WebRequest.Create(ApiUrl);
            request.Method = "GET";
            request.ContentType = "application/json";

            using (var response1 = request.GetResponse())
            {
                using (var reader = new StreamReader(response1.GetResponseStream()))
                {
                    responseString = reader.ReadToEnd();
                }
            }
            
            return responseString;

        }

    }
}