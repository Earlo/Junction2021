namespace Loupedeck.DemoPlugin
{
    using System;

    public class DemoApplication : ClientApplication
    {
        public DemoApplication()
        {

        }

        protected override String GetProcessName() => "Junction";

        protected override String GetBundleName() => "Junction";
    }
}