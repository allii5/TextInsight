import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './LoginScreen/LoginPage';
import SignUp from './SignUpScreen/SignUpPage';
import './App.css';
import FirstLogin from './FirstLoginScreen/FirstLogin';
import EmailVerification from './EmailVerificationScreen/EmailVerification';
import UpdatePassword from './UpdatePassword/UpdatePassword';
import StudentDashboard from './DashboardScreens/StudentDashboard';
import EssaySubmission from './EssaySubmission/EssaySubmission';
import SubmittedEssay from './SubmittedEssayDetails/SubmittedEssay';
import Notifications from './NotificationScreen/Notifications';
import Sidebar from './Sidebar/Sidebar';
import TeacherSidebar from './TeacherSidebar/TeacherSidebar';
import Navbar from './NavBar/Navbar';
import EssayEvolution from './EssayEvolutionScreen/EssayEvolution'
import ProgressMonitoring from './ProgressMonitoringScreen/ProgressMonitoring';
import ManageEssays from './ManageEssaysScreen/ManageEssays';
import SubmissionHistory from './SubmissionHistoryScreen/SubmissionHistory';
import FeedbackHistory from './FeedbackHistoryScreen/FeedbackHistory';
import EssayInsight from './EssayInsightScreen/EssayInsight';
import ExploreInsight from './ExploreInsightScreen/ExploreInsight';
import TeacherFeedbackHistoryExpand from './TeacherFeedbackHistoryExpand/TeacherFeedbackHistoryExpand';
import TeacherProgressHistoryExpand from './TeacherProgressMonitoringExpand/TeacherProgressMonitoringExpand';
import TeacherSubmissionHistoryExpand from './TeacherSubmissionHistoryExpand/TeacherSubmissionHistoryExpand';
import TeacherEssayEvolution from './TeacherEssayEvolution/TeacherEssayEvolution';
import TeacherEssayInsight from './TeacherEssayInsight/TeacherEssayInsight';
import TeacherDashboard from './TeacherDashboard/TeacherDashboard';
import TeacherManageEssays from './TeacherManageEssays/TeacherManageEssays';
import TeacherManageClasses from './TeacherManageClasses/TeacherManageClasses';
import TeacherSubmissionHistory from './TeacherSubmissionHistoryScreen/TeacherSubmissionHistory';
import TeacherFeedbackHistory from './TeacherFeedbackHistoryScreen/TeacherFeedbackHistoryScreen';
import TeacherProgressMonitoring from './TeacherProgressMonitoringScreen/TeacherProgressMonitoring';
import TeacherSubmittedEssayDetails from './TeacherSubmittedEssayDetails/TeacherSubmittedEssayDetails';
import TeacherExploreInsight from './TeacherExploreInsight/TeacherExploreInsight';
import CreateClass from './CreateClass/CreateClass';
import UpdateClass from './UpdateClass/UpdateClass';
import CreateEssay from './CreateEssay/CreateEssay';
import UpdateEssay from './UpdateEssay/UpdateEssay';
import AccountCreation from './AccountCreation/AccountCreation';
import LoadingAnimation from './LoadingAnimation/LoadingAnimation';
import FloatAnimation from './FloatAnimation/FloatAnimation';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/updatepassword" element={<UpdatePassword />} />
        <Route path="/emailverification" element={<EmailVerification />} />
        <Route path="/navbar" element={<Navbar />} />
        <Route path="/sidebar" element={<Sidebar />} />
        <Route path="/teachersidebar" element={<TeacherSidebar/>} />
        <Route path="/studentdashboard" element={<StudentDashboard />} />
        <Route path="/manageessays" element={<ManageEssays />} />
        <Route path="/submissionhistory" element={<SubmissionHistory />} />
        <Route path="/feedbackhistory" element={<FeedbackHistory />} />
        <Route path="/progressmonitoring" element={<ProgressMonitoring />} />
        <Route path="/essayevolution" element={<EssayEvolution />} />
        <Route path="/essayinsight" element={<EssayInsight />} />
        <Route path="/exploreinsight" element={<ExploreInsight />} />
        <Route path="/essaysubmission" element={<EssaySubmission />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/submittedessay" element={<SubmittedEssay />} />
        <Route path="/submissionhistory" element={<SubmissionHistory />} />
        <Route path="/firstlogin" element={<FirstLogin />} />
        <Route path="/teachersubmissionhistoryexpand" element={<TeacherSubmissionHistoryExpand />} />
        <Route path="/teacherfeedbackhistoryexpand" element={<TeacherFeedbackHistoryExpand />} />
        <Route path="/teacherprogresshistoryexpand" element={<TeacherProgressHistoryExpand />} />
        <Route path="/teacheressayevolution" element={<TeacherEssayEvolution />} />
        <Route path="/teacheressayinsight" element={<TeacherEssayInsight />} />
        <Route path="/teacherdashboard" element={<TeacherDashboard/>}/>
        <Route path="/teachermanageessays" element={<TeacherManageEssays />} />
        <Route path="/teachermanageclasses" element={<TeacherManageClasses />} />
        <Route path="/teachersubmissionhistory" element={<TeacherSubmissionHistory />} />
        <Route path="/teacherprogressmonitoring" element={<TeacherProgressMonitoring />} />
        <Route path="/teacherfeedbackhistory" element={<TeacherFeedbackHistory />} />
        <Route path="/teachersubmittedessaydetails" element={<TeacherSubmittedEssayDetails />}/>
        <Route path="/teacherexploreinsight" element={<TeacherExploreInsight/>}/>
        <Route path="/updateclass" element={<UpdateClass />} />
        <Route path="/createclass" element={<CreateClass />} />
        <Route path="/updateessay" element={<UpdateEssay />} />
        <Route path="/createessay" element={<CreateEssay />} />
        <Route path="/accountcreation" element={<AccountCreation />} />
        <Route path="/loadinganimation" element={<LoadingAnimation />} />
        <Route path="/floatanimation" element={<FloatAnimation />} />



      </Routes>
    </Router>




  );
}

export default App;
