const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  try {
    return new Promise((resolve, reject) => {
      cloudant
        .postDocument({
          db: "reviews",
          document: params.review,
        })
        .then(() => {
          resolve({ wasSuccessful: true });
        })
        .catch((err) => {
          console.log(err);
          reject({ err: err });
        });
    });
  } catch (error) {
    return { error: error.description };
  }
}
